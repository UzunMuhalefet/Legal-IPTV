<?php

// Step 1: Take the "id" query string parameter from the incoming request
$id = $_GET['id'] ?? null;

// Check if id parameter exists
if ($id === null) {
    http_response_code(404);
    die("ID parameter is missing");
}

// Step 2: Send a request to "https://kocaeliyiseyret.com/Kamera/Index//" by adding the id value to the end of the URL.
$url = "https://kocaeliyiseyret.com/Kamera/Index/{$id}";

// Send a GET request to the URL
$response = file_get_contents($url);

// Check if response is valid
if ($response === false) {
    http_response_code(404);
    die("Failed to fetch data from remote server");
}

// Step 3: Find the iframe tags in the response of Step 2 and get the src value of it
if (!preg_match('/<iframe.*?src="(.*?)".*?>/i', $response, $matches)) {
    http_response_code(404);
    die("Unable to find iframe src");
}

$iframeSrc = $matches[1];

// Step 4: Replace "player.tvkur.com" with "content.tvkur.com" and add "/master.m3u8" to the result of Step 3
$newSrc = str_replace("player.tvkur.com", "content.tvkur.com", $iframeSrc);
$newSrc .= "/master.m3u8";

// Step 5: Redirect to the result of Step 4
header("Location: $newSrc");
exit;
