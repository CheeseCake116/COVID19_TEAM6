<?php
$link = mysqli_connect("localhost", "userid", "password", "databasename");
// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
//echo "Connect Successfully. Host info: " . mysqli_get_host_info($link) . "\n";

?>
