<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class ROUTE extends CI_Controller
{
    //主函数部分
    public function index()
    {
        //不传参数=随机返回
        //传城市=城市搜索
        //传城市+日期=城市日期搜索
        //只传id=精确搜索
        $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
        $user = 'mc';
        $db   = 'cauth';
        $pass = 'Westbrook0';
        if(isset($_GET['city'])){
            $sql='SELECT * FROM citytours where city =\''.$_GET['city']."' ";
            if(isset($_GET['days'])){
                $sql=$sql."and days = ".$_GET['days'];
            }
        }
        elseif(isset($_GET['id'])){
            $sql='SELECT * FROM citytours where id =\''.$_GET['id']."' ";
        }
        else{
            $sql='SELECT * FROM citytours';
        }
        $conn = mysqli_connect($host, $user, $pass, $db);
        if(!$conn){
            die("连接失败: " . mysqli_connect_error());
        }
        $result = mysqli_query($conn, $sql);
        $count=4;
        if($result){
            if (mysqli_num_rows($result) < 4) {
                $count=mysqli_num_rows($result);
            }
            $arr=array();
            //echo $count;
            for($i=0;$i<$count;$i++){
                $record=mysqli_fetch_assoc($result);
                $arr[]=$record;
            }
            mysqli_close($conn);
            echo '{"routes":'.json_encode($arr)."}";
        }
    }
}
