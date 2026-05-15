const { execFileSync } = require("node:child_process");
const { existsSync } = require("node:fs");
const path = require("node:path");
const process = require("node:process");

const config = require("./markdownlint.config.js");

const repoRoot = path.resolve(__dirname, "..");
const markdownlintCli = path.join(repoRoot, "node_modules", "markdownlint-cli", "markdownlint.js");

process.chdir(repoRoot);

async function main() {
  let lint;
  try {
    ({ lint } = require("markdownlint/promise"));
  } catch {
    console.warn("markdownlint: node_modules 가 없습니다. `npm ci` 를 먼저 실행하세요.");
    return;
  }

  const args = process.argv.slice(2);
  const shouldWrite = args.includes("--write");
  const isStaged = args.includes("--staged");
  const targets = isStaged ? getStagedMarkdownFiles() : getTrackedMarkdownFiles();

  if (targets.length === 0) {
    console.log("markdownlint: 대상 Markdown 파일이 없습니다.");
    return;
  }

  if (shouldWrite) {
    applyFixes(targets);
  }

  const result = await lint({
    files: targets,
    config,
  });

  const warnings = formatWarnings(result);
  if (warnings.length === 0) {
    console.log(`markdownlint: warning 없음 (${targets.length} files)`);
    return;
  }

  warnings.forEach((warning) => console.warn(warning));
  console.warn(`markdownlint: ${warnings.length} warnings (${targets.length} files checked)`);
}

function getStagedMarkdownFiles() {
  return runGit(["diff", "--cached", "--name-only", "--diff-filter=ACM", "--", "*.md"]).filter(
    (filePath) => existsSync(filePath)
  );
}

function getTrackedMarkdownFiles() {
  return runGit(["ls-files", "*.md"]).filter((filePath) => existsSync(filePath));
}

function applyFixes(targets) {
  try {
    execFileSync(
      process.execPath,
      [markdownlintCli, "--fix", "--config", "scripts/markdownlint.config.js", ...targets],
      {
        cwd: repoRoot,
        stdio: "inherit",
      }
    );
  } catch (error) {
    if (error && typeof error === "object" && "status" in error && error.status === 1) {
      return;
    }

    throw error;
  }
}

function runGit(args) {
  const output = execFileSync("git", args, {
    cwd: repoRoot,
    encoding: "utf8",
  });

  return output
    .split(/\r?\n/u)
    .map((line) => line.trim())
    .filter(Boolean);
}

function formatWarnings(result) {
  const warnings = [];

  for (const [filePath, entries] of Object.entries(result)) {
    const relativePath = path.relative(repoRoot, path.resolve(repoRoot, filePath));
    for (const entry of entries) {
      const column = Array.isArray(entry.errorRange) ? entry.errorRange[0] : 1;
      const detail = entry.errorDetail ? ` ${entry.errorDetail}` : "";
      warnings.push(
        `${relativePath}:${entry.lineNumber}:${column} warning ${entry.ruleNames[0]} ${entry.ruleDescription}${detail}`
      );
    }
  }

  return warnings;
}

main().catch((error) => {
  console.error("markdownlint 실행 실패");
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
