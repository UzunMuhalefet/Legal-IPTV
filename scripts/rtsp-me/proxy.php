<?php
// Step 1: Get the "id" query string from the URL
$id = $_GET['id'] ?? '';

// Step 2: Place the value of Step 1 into the id part of the URL
$url = "https://rtsp.me/embed/$id/";

// Step 3: Send a request to that URL
$response = file_get_contents($url);

// Step 4: Find the URL that starts with https:// and ends with "m3u8"
preg_match('/https:\/\/(.*?).m3u8/', $response, $matches);
$final_url = $matches[0];

// Step 5: Redirect to the final URL
header("Location: $final_url");
exit;
?>