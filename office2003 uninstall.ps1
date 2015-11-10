$office=Get-WmiObject -Class win32_product | where {$_.caption -like "*office*"}
$2003=$office|where{$_.name -like "*2003*"}
$2003
$2003.Uninstall()