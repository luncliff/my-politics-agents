#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Fetch NVIDIA Nemotron-Personas-Korea parquet shards into archive/raw.

.DESCRIPTION
    Wraps `python -m nemotron_personas.fetch`. By default runs --dry-run; pass
    -Confirm to actually download (~2 GB).
#>
[CmdletBinding()]
param(
    [switch]$Confirm,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$cmd = @("uv", "run", "python", "-m", "nemotron_personas.fetch")
if (-not $Confirm) { $cmd += "--dry-run" }
if ($Force)        { $cmd += "--force" }

Write-Host "› $($cmd -join ' ')"
& $cmd[0] @($cmd[1..($cmd.Length - 1)])
