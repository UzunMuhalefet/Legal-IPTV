<?php
// Step 1: Get the "id" query string from the URL
$id = $_GET['id'] ?? '';

// Step 2: Place the value as a subdomain of .click2stream.com
$url = "https://$id.click2stream.com";

// Step 3: Send a request to that URL
$response = file_get_contents($url);

// Check if request was successful
if ($response === false) {
    // If request fails, return 404 with explanation
    http_response_code(404);
    exit("Error: Failed to retrieve data from the specified URL.");
}

// Step 4: Find the id value
if (!preg_match_all('/id:\s*"\K[a-zA-Z0-9]+/', $response, $matches)) {
    http_response_code(404);
    exit;
}
$angelcam_id = end($matches[0]); // Get the last match

// Step 5: Send a POST request to Angelcam API
$data = json_encode([
    'domain' => $url
]);
$options = [
    'http' => [
        'method' => 'POST',
        'header' => "Content-Type: application/json\r\n" .
                    "authority: my.angelcam.com",
        'content' => $data
    ]
];
$angelcam_url = "https://my.angelcam.com/broadcasting/api/domain-lock-validation/$angelcam_id/";
$angelcam_response = file_get_contents($angelcam_url, false, stream_context_create($options));

// Check if Angelcam API request was successful
if ($angelcam_response === false) {
    // If Angelcam API request fails, return 404 with explanation
    http_response_code(404);
    exit("Error: Failed to validate domain with Angelcam API.");
}

// Step 6: Parse the response and get the "token" value
$angelcam_data = json_decode($angelcam_response, true);
if (!isset($angelcam_data['token'])) {
    // If token is not found in the response, return 404 with explanation
    http_response_code(404);
    exit("Error: Token not found in the response from Angelcam API.");
}
$token = $angelcam_data['token'];

// Step 7: Send a GET request to https://v.angelcam.com/iframe
$iframe_url = "https://v.angelcam.com/iframe?v=$angelcam_id&token=$token";
$iframe_response = file_get_contents($iframe_url);

// Check if iframe request was successful
if ($iframe_response === false) {
    // If iframe request fails, return 404 with explanation
    http_response_code(404);
    exit("Error: Failed to retrieve iframe data from Angelcam.");
}

// Step 8: Get the value of source from the response text
if (!preg_match('/source:\s*\'(.*?)\'/', $iframe_response, $matches)) {
    // If source is not found in the response, return 404 with explanation
    http_response_code(404);
    exit("Error: Source URL not found in the response from Angelcam.");
}
$source_url = $matches[1];

// Step 9: Redirect to the source URL
header("Location: $source_url");
exit;
?>
