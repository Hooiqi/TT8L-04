<?php>
if($_SERVER["REQUEST_METHOD"]=="POST"{
   $email = $_POST['email'];
   $password = $_POST['password'];

   $redirectMap = array(
     'admin' => 'admin_dashboard.html'
     'user' => 'userpage.html' );

   if 
