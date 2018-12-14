<?php

require 'vendor/autoload.php';

use SMSGatewayMe\Client\ApiClient;
use SMSGatewayMe\Client\Configuration;
use SMSGatewayMe\Client\Api\MessageApi;
use SMSGatewayMe\Client\Model\SendMessageRequest;

// Configure client
$config = Configuration::getDefaultConfiguration();
$config->setApiKey('Authorization', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhZG1pbiIsImlhdCI6MTUzMTkyODA3OSwiZXhwIjo0MTAyNDQ0ODAwLCJ1aWQiOjU2OTE4LCJyb2xlcyI6WyJST0xFX1VTRVIiXX0.qj5ADOL2yOKF4VUyrKjsj89FhIfmS8n-bNvhnbOAdW4');
$apiClient = new ApiClient($config);
$messageClient = new MessageApi($apiClient);

// Sending a SMS Message
$sendMessageRequest1 = new SendMessageRequest([
    'phoneNumber' => '089515377627',
    'message' => 'test1',
    'deviceId' => 96428
]);
$sendMessages = $messageClient->sendMessages([
    $sendMessageRequest1
]);
print_r($sendMessages);