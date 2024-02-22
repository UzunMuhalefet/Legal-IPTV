<?php

// Step 1: Get the "id" query string parameter from the incoming request
$id = $_GET['id'];

// Step 2: Send a request to https://www.earthtv.com/en/webcam/ with proper headers
$url = "https://www.earthtv.com/en/webcam/$id";
$headers = [
    "X-Client-Ip: " . $_SERVER['REMOTE_ADDR'],
    "X-Forwarded-For: " . $_SERVER['REMOTE_ADDR']
];
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Check if the response is successful
if ($status_code != 200) {
    http_response_code(404);
    die("Error: Unable to fetch data from EarthTV");
}

// Step 3: Extract token using regex
if (!preg_match('/token:\s\'(.*?)\'/', $response, $matches)) {
    http_response_code(404);
    die("Error: Unable to extract token from EarthTV response");
}
$token = $matches[1];

// Step 4: Send a request to https://livecloud.earthtv.com/api/v1/media.getPlayerConfig with proper headers
$configUrl = "https://livecloud.earthtv.com/api/v1/media.getPlayerConfig?playerToken=$token";
$headers[] = "Referer: https://player.earthtv.com/";
$ch = curl_init($configUrl);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$configResponse = curl_exec($ch);
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Check if the response is successful
if ($status_code != 200) {
    http_response_code(404);
    die("Error: Unable to fetch player configuration from EarthTV API");
}

// Step 5: Parse JSON response and get the HLS stream URL
$configData = json_decode($configResponse, true);
if (!isset($configData['streamUris']['hls'])) {
    http_response_code(404);
    die("Error: HLS stream URL not found in EarthTV API response");
}
$hlsStreamUrl = $configData['streamUris']['hls'];

// Step 6: Redirect to HLS stream URL
header("Location: $hlsStreamUrl");
exit;
?>
