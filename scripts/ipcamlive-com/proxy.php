<?php
// Step 1: Get the "id" query string from the URL
$id = $_GET['id'] ?? '';

// Step 2: Place the value of Step 1 into the end of this URL
$url = "https://ipcamlive.com/player/player.php?alias=$id";

// Step 3: Send a request to that URL
$response = file_get_contents($url);

// Step 4: Find the part that starts with "var address = 'http://" and ends with "/"
if (preg_match('/var\s+address\s*=\s*\'(http:\/\/.*?)\//', $response, $matches)) {
    $address = $matches[1];
} else {
    http_response_code(404);
    exit;
}

// Step 5: Find the part that starts with "var streamid = '" and ends with "'"
if (preg_match('/var\s+streamid\s*=\s*\'(.*?)\'/', $response, $matches)) {
    $streamid = $matches[1];
} else {
    http_response_code(404);
    exit;
}

// Step 6: Build URL
$final_url = $address . "/streams/" . $streamid . "/stream.m3u8";

// Redirect to the final URL
header("Location: $final_url");
exit;
?>

