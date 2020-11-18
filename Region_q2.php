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
    th, td {
        border: 1px solid #444444;
    }
</style>
<body>
    <h1 style="text-align:center"> 데이터베이스 팀 프로젝트 6조 </h1>
    <h2 style="text-align:center"> 곽진욱, 곽승규, 이주형 </h2>
    <hr style = "border : 5px solid yellowgreen">
    
    <h3> City를 입력하세요 </h3>
    <form action="" method="post">
        <select name ="City">
            <option value ="none" selected> 선택하세요 </option>
            <?php
                $sql = "select distinct city from region";
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
        $city = $_POST['City'];
        $sql="select count(*) as num from region where city = '". $city."'";
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
            print "selected city = " . $city;
            $sql = "select * from region where city = '".$city."'";
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
