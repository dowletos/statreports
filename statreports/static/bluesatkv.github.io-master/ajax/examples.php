<?php

// Basic example of PHP script to handle with jQuery-Tabledit plug-in.
// Note that is just an example. Should take precautions such as filtering the input data.
header('Content-Type: application/json');

// CHECK REQUEST METHOD
if ($_SERVER['REQUEST_METHOD']=='POST') {
  $input = filter_input_array(INPUT_POST);
} else {
  $input = filter_input_array(INPUT_GET);
}

// PHP QUESTION TO MYSQL DB
if ($input['action'] === 'edit') {


} else if ($input['action'] === 'delete') {


} else if ($input['action'] === 'restore') {


}

// RETURN OUTPUT
echo json_encode($input);

?>