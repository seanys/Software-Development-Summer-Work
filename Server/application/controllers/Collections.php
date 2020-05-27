<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接
class Collections extends CI_Controller
{  //action 1=>储存 2=>删除 3=>查询
    //主函数部分
    public function index()
    {
        if(isset($_GET['action'])){  //储存数据,action=1，其余数据必须要传，可空
            if($_GET['action']=='1'){
                $timee=date('Y-m-d H:i:s');
                $temp=DB::insert('collection', [
                    'user_id' => $_GET['user_id'],
                    'type' => $_GET['type'],
                    'content' => $_GET['content'],
                    'fromcity' => $_GET['fromcity'],
                    'tocity' => $_GET['tocity'],
                    'id' => $timee
                ]);
                    if($temp){
                        echo $timee;
                    }
            }
            elseif ($_GET['action']=='2'){ //删除数据，action填入2，然后必须传id
                $temp=DB::delete('collection', [
                    'id' => $_GET['id']
                ]);
                if($temp){
                    echo "delete succeed";
                }
                else{
                    echo "delete failed";
                }
            }
            elseif($_GET['action']=='3'){  //查询数据，action填入3：
                $arr=array();
                $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
                $user = 'mc';
                $db   = 'cauth';
                $pass = 'Westbrook0';
                $sql="SELECT *
                from collection where user_id= '".$_GET['user_id']."'";
                if(isset($_GET['type'])){
                    $sql=$sql."and type = '".$_GET['type']."'";
                }
                if(isset($_GET['fromcity'])){
                    $sql=$sql."and fromcity = '".$_GET['fromcity']."'";
                }
                if(isset($_GET['tocity'])){
                    $sql=$sql."and tocity = '".$_GET['tocity']."'";
                }
                $conn = mysqli_connect($host, $user, $pass, $db);
                if(!$conn){
                    die("连接失败: " . mysqli_connect_error());
                }
                $result = mysqli_query($conn, $sql);
                if($result){
                    for($i=0;$i<mysqli_num_rows($result);$i++){
                        $record=mysqli_fetch_assoc($result);
                        $arr[]=$record;
                    }
                    echo json_encode($arr);
                }
            }
        }
    }
}