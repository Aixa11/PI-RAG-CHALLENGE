function Invoke-RestMethodUtf8 {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Uri,

        [Parameter()]
        [string]$Method = "GET",

        [Parameter()]
        [string]$Body = $null
    )

    $params = @{
        Uri             = $Uri
        Method          = $Method
        UseBasicParsing = $true
        Headers         = @{
            "Accept" = "application/json; charset=utf-8"
        }
    }

    if ($Body) {
        $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
        $params["Body"] = $utf8Bytes
        $params["ContentType"] = "application/json; charset=utf-8"
    }

    $response = Invoke-WebRequest @params
    $jsonText = [System.Text.Encoding]::UTF8.GetString($response.RawContentStream.ToArray())
    return $jsonText | ConvertFrom-Json
}