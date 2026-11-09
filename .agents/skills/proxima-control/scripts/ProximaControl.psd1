# ProximaControl.psd1 - wp1285 r1 (PROXIMA-P1-S3). Pure data manifest for the sibling ProximaControl.psm1 (S2): nine keys only.
# No NestedModules/RequiredModules/ScriptsToProcess: S1 ProximaConfig.psm1 is still loaded only by the S2 hash-before-import guard.
@{
    RootModule           = 'ProximaControl.psm1'
    ModuleVersion        = '2.0.0'
    GUID                 = '7f7055d6-51e3-4fb8-bbeb-7851a739bfb6'
    PowerShellVersion    = '5.1'
    CompatiblePSEditions = @('Desktop', 'Core')
    FunctionsToExport    = @('px', 'Invoke-ProximaOperation')
    CmdletsToExport      = @()
    VariablesToExport    = @()
    AliasesToExport      = @()
}
