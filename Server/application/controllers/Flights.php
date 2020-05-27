<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Flights extends CI_Controller
{
    //主函数部分
    public function index()
    {
        $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
        $user = 'mc';
        $db   = 'cauth';
        $pass = 'Westbrook0';
        $sql='SELECT * FROM flights,canbins where flights.id = canbins.id and departureDate BETWEEN \''.$_GET['earlyTime']."' and '".$_GET['laterTime'].
        "' and departureCityName in".$this->city($_GET['from'])." and arrivalCityName in ".$this->city($_GET['to']);
        //echo $sql;
        if(isset($_GET['minprice'])){
            $sql=$sql." and price > ".$_GET['minprice'];
        }
        if(isset($_GET['maxprice'])){
            $sql=$sql." and price < ".$_GET['maxprice'];
        }
        if(isset($_GET['rank'])){
            $sql=$sql." order by canbins.price";
        }
        //echo $sql;
        $conn = mysqli_connect($host, $user, $pass, $db);
        if(!$conn){
            die("连接失败: " . mysqli_connect_error());
        }
        $result = mysqli_query($conn, $sql);
        $count=40;
        if($result){
            if (mysqli_num_rows($result) < 40) {
                $count=mysqli_num_rows($result);
            }
            $arr=array();
            //echo $count;
            for($i=0;$i<$count;$i++){
                $record=mysqli_fetch_assoc($result);
                $arr[]=$record;
            }
            mysqli_close($conn);
            echo '{"flights":'.json_encode($arr)."}";
        }
    }
    protected function city($city){
        $airpots;
        switch ($city){
        case "上海城区":
        return "('虹桥国际机场','浦东国际机场')";
        break;
        case "西安市":
        return "('咸阳国际机场')";
        break;
        case "北京城区":
        return "('首都国际机场')";
        break;
        default:
        return null;
        }
    }
}