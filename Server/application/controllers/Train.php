<?php
defined('BASEPATH') or exit('No direct script access allowed');

use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Train extends CI_Controller{

    public function index()
    {
        //header("content-type:text/html; charset=utf-8");
        $fromCode;
        $toCode;
        if((isset($_GET['from_city'])) and (isset($_GET['to_city']))){
            $fromCode=$this->findCode($_GET['from_city']);
            $toCode=$this->findCode($_GET['to_city']);
        }

        $date=$_GET['date'];

        //echo $fromCode["code"]; //出发站代码
        //echo $toCode["code"]; //到达站代码
        
        $from=$fromCode["code"]; //查询车站列表
        $to=$toCode["code"];
        $url="https://www.12306.cn/kfzmpt/lcxxcx/query?purpose_codes=ADULT&queryDate=$date&from_station=$from&to_station=$to";
        $ticketsLeft=$this->query($url);  //将json读成一个数组类型的数据
        if($ticketsLeft["data"]["flag"]==false){
            die("query error");
        }
        //echo $ticketsLeft["data"]["datas"][0]["train_no"];
        $from_station_unique=array();
        $to_station_unique=array();
        for($i=0;$i<count($ticketsLeft["data"]["datas"]);$i++){
            array_push($from_station_unique,$ticketsLeft["data"]["datas"][$i]['from_station_name']);
            array_push($to_station_unique,$ticketsLeft["data"]["datas"][$i]['to_station_name']);
        }
        $from_station_unique=array_unique($from_station_unique);
        $to_station_unique=array_unique($to_station_unique);
        //var_dump(json_decode($result));

        //print_r($from_station_unique);             //输出两座城市所有可用车站
        //print_r($to_station_unique);
        
        
        $timeCost = array();
        for($i=0;$i<count($ticketsLeft["data"]["datas"]);$i++) {
            $timeCost[] = $ticketsLeft["data"]["datas"][$i]['lishiValue'];
        }
        array_multisort($timeCost, SORT_ASC, $ticketsLeft["data"]["datas"]);   //按历时由短到长排序

        //print_r($ticketsLeft["data"]["datas"]);

        $trainList=array();

        for($i=0;$i<count($ticketsLeft["data"]["datas"]) and $i<4;$i++) {  //最快的4个车次的站序信息
            $tid=$ticketsLeft['data']['datas'][$i]['train_no'];
            $url="https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=$tid&from_station_telecode=$from&to_station_telecode=$to&depart_date=$date";
            //echo $url;
            $res=$this->query($url);
            //print_r($res);
            if(!$res['status']){
                die("query error");
            }

            $flag=true;
            for($j=0;$j<count($res["data"]["data"]) and $flag;$j++) {
                if(!strcmp($res["data"]["data"][$j]["station_name"],$ticketsLeft["data"]["datas"][$i]["from_station_name"])){
                    $fromNo=$res["data"]["data"][$j]["station_no"];
                    //$ticketsLeft["data"]["datas"][$i]["start_time"]=$res["data"]["data"][$j]['start_time'];
                    //echo "find1";
                    //echo $res["data"]["data"][$j]["station_name"];
                    //echo $ticketsLeft["data"]["datas"][$i]["from_station_name"];
                    $flag=false;
                }
            }
            $flag=true;
            for(;$j<count($res["data"]["data"]) and $flag;$j++) {
                if(!strcmp($res["data"]["data"][$j]["station_name"],$ticketsLeft["data"]["datas"][$i]["to_station_name"])){
                    $toNo=$res["data"]["data"][$j]["station_no"];
                    //$ticketsLeft["data"]["datas"][$i]["arrive_time"]=$res["data"]["data"][$j]['arrive_time'];
                    //echo "find2";
                    //echo $res["data"]["data"][$j]["station_name"];
                    //echo $ticketsLeft["data"]["datas"][$i]["to_station_name"];
                    $flag=false;
                }
            }
            if(!$flag){
                //echo $fromNo;
                //echo $toNo;
            }
            else{
                die("error");
            }
            
            $flag=true;
            $temp=$ticketsLeft['data']['datas'][$i]['train_no'];
            $url="https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=$temp&from_station_no=$fromNo&to_station_no=$toNo&seat_types=O&train_date=$date";
            //echo $url;
            $price=$this->query($url);
            //print_r($price);
            if(isset($price['data']["O"])){
                $ticketsLeft["data"]["datas"][$i]['type']='二等座';
                $ticketsLeft["data"]["datas"][$i]['price']=$price['data']["O"];
            }
            $temp=$ticketsLeft['data']['datas'][$i]['train_no'];
            $url="https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=$temp&from_station_no=$fromNo&to_station_no=$toNo&seat_types=A3&train_date=$date";
            //echo $url;
            //print_r($price);
            $price=$this->query($url);
            if(isset($price['data']["A3"])){
                $ticketsLeft["data"]["datas"][$i]['type']='硬座';
                $ticketsLeft["data"]["datas"][$i]['price']=$price['data']["A3"];
            }
            //echo $ticketsLeft["data"]["datas"][$i]['type'];
            //echo $ticketsLeft["data"]["datas"][$i]['price'];
            if(isset($ticketsLeft["data"]["datas"][$i]['type'])){
                //echo $ticketsLeft["data"]["datas"][$i];
                array_push($trainList,$ticketsLeft["data"]["datas"][$i]);
            }
        }
        echo json_encode($trainList);
        
        //print_r($ticketsLeft["data"]["datas"]);


        //fclose($fp);
    }

    protected function query($url){  //从接口读数据
        $context_options = array(
            'http' =>
             array(
              'method' => "GET",
              'header' => "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\nReferer:https://www.12306.cn/\r\n",
             ));
        $context = stream_context_create($context_options);
        //获取资源
        $res = file_get_contents($url,FALSE,$context);
        //echo $res;
        return json_decode($res,true);
        /*$fp = fopen($url, "r");
        $stream_meta = stream_get_meta_data($fp);
        print_r($stream_meta);
        $result = "";
        while (!feof($fp)) {
        $result .= fgets($fp, 1024);
        }
        $array=json_decode($result,true); 
        fclose($fp);
        return $array; */
    }

    protected function findCode($name){  //取得城市对应车站代码
        $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
        $user = 'mc';
        $db   = 'cauth';
        $pass = 'Westbrook0';
        $sql='SELECT name,code FROM train_station_code where locate(name,"'.$name.'")';
        $conn = mysqli_connect($host, $user, $pass, $db);
        if(!$conn){
            die("连接失败: " . mysqli_connect_error());
        }
        $result1 = mysqli_query($conn, $sql);

        if($result1){
            $record=mysqli_fetch_assoc($result1);
            mysqli_close($conn);
            return $record;
        }
        else{
            return -1;
        }
    }

}