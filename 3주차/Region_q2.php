<head>
    <title> K_COVID19 TEAM6 </title>
</head>
<?php
    $link = mysqli_connect("127.0.0.1","tmdrb0912","0206", "k_covid19");
    if( $link === false )
    {
        die("ERROR: Could not connect. " . mysqli_connect_error());
    }
    echo "Coneect Successfully. Host info: " . mysqli_get_host_info($link) . "\n";
?>
<style>
    table {
        width: 100%;
        border: 1px solid #444444;
        border-collapse: collapse;
    }

    th,
    td {
        border: 1px solid #444444;
    }

    h1,
    h2 {
        text-align: center;
    }
</style>
<body>
    <h1> 데이타베이스 6조 </h1>
    <h2>곽진욱, 곽승규, 이주형</h2>
    <hr style="border : 5px solid yellowgreen">
    
    <h3> Province를 입력하세요 </h3>
    <form action="" method="post">
        <select name ="Province">
            <option value ="none" selected> 선택하세요 </option>
            <option value ="all">all </option>
            <?php
                $sql = "select distinct province from region";
                $res = mysqli_query($link, $sql);
                while ($row = mysqli_fetch_assoc($res)) {
                
                    foreach ($row as $key => $val) {
                        print "<option value=" . $val . ">" . $val . "</option>";
                    }
                }
            ?>
        </select>
        <input type="submit" value="load" name="button"/>
    </form>

    <?php
        $province = 'all';
        if ( !empty($_POST) ) // 값이 있으면 
            $province = $_POST['Province'];
        
        $sql= "select count(*) as num from region"; // 초기값 

        if ( $province == 'all')
            $sql= "select count(*) as num from region";
        else if (!empty($_POST))
            $sql="select count(*) as num from region where province = '". $province."'";
        $result = mysqli_query($link, $sql);
        $data = mysqli_fetch_assoc($result);
    ?>
    <p>
        <h3>Region table (Currently <?php echo $data['num']; ?>) patients in database </h3>
    </p>

    <table cellspacing="0" width="100%">
        <thead>
        <tr>
            <th>Region_code</th>
            <th>Province</th>
            <th>City</th>
            <th>Latitude</th>
            <th>Longtitude</th>
            <th>elementary_school_count</th>
            <th>kindergarten_count</th>
            <th>university_count</th>
            <th>academy_ratio</th>
            <th>elderly_population_ratio</th>
            <th>elderly_alone_ratio</th>
            <th>nursing_home_count</th>
        </tr>
        </thead>
        <tbody>
            <?php
            print "<h3>". "selected province : ". $province ."</h3>" ;
            if ($province == 'all')
                $sql = "select * from region";
            else
                $sql = "select * from region where province = '".$province."'";
            $result = mysqli_query($link,$sql);
                    while( $row = mysqli_fetch_assoc($result)  )
                    {
                        print "<tr>";
                        foreach($row as $key => $val)
                        {
                            print "<td>" . $val . "</td>";
                        }
                        print "</tr>";
                    }
            ?>
        </tbody>
    </table>


</body>
