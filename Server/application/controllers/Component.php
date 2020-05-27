<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Component extends CI_Controller
{
    //主函数部分
    public function index()
    {
        $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
        $user = 'mc';
        $pass = 'Westbrook0';
        $db   = 'aircraft';
        $conn = mysqli_connect($host, $user, $pass, $db);
        if(!$conn){
            die("连接失败: " . mysqli_connect_error());
        }
        
        $product = mysqli_fetch_assoc(mysqli_query($conn, 'SELECT * FROM products where product_id = '.$_GET['product_id']));
        $product_image = mysqli_fetch_assoc(mysqli_query($conn, 'SELECT * FROM product_image where product_id = '.$_GET['product_id']));
        $product_page = mysqli_fetch_assoc(mysqli_query($conn, 'SELECT * FROM product_page where product_id = '.$_GET['product_id']));

        $this->json([
            'code' => 1,
            'data' => [
                "product"=>$product,
                "product_image"=>$product_image,
                "product_page"=>$product_page
            ],
        ]);

        mysqli_close($conn);
    }
}