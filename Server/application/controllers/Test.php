<?php
defined('BASEPATH') or exit('No direct script access allowed');

use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Test extends CI_Controller
{
    //主函数部分
    public function index()
    {
        $url="https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=5n0000G3560G&from_station_telecode=XMS&to_station_telecode=TXK&depart_date=2019-09-06";
        $res=$this->query($url);
            //$res=file_get_contents($url);
            //$res=$this->query($url);
            //echo $res;
        print_r($res);

        if (isset($_GET['test'])){
            $this->json([
                'code' => "success",
                'data' => [
                    "infor" => "test请求的值为".$_GET['test']
                ],
            ]);
        }else{
            $this->json([
                'code' => "success",
                'data' => [
                    "infor" => "测试成功"
                ],
            ]);
        }
    }

    //其他的函数，面向对象
    protected function generateRandomString()
    {
        $length = 30;
        $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $randomString = '';
        for ($i = 0; $i < $length; $i++) {
            $randomString .= $characters[rand(0, strlen($characters) - 1)];
        }
        return $randomString;
    }

    protected function query($url){  //从接口读数据
        $fp = fopen($url, "r");
        stream_get_meta_data($fp);
        $result = "";
        while (!feof($fp)) {
        $result .= fgets($fp, 1024);
        }
        $array=json_decode($result,true); 
        fclose($fp);
        return $array; 
    }
}
