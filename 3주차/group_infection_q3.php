<head>
    <title> K_COVID19 TEAM6 </title>
</head>
<?php
$link = mysqli_connect("127.0.0.1", "juhyoung98", "0000", "k_covid19");
if ($link === false) {
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
    <h3> Select Province and Month.</h3>
    <?php
        $sql = "CREATE OR REPLACE view GROUP_INFECTION(Infection_case, Province, First_Confirmed_Date, Total_confirmed_count) as
        select C.infection_case, C.province, min(confirmed_date), C.confirmed
        from Patientinfo P, caseINFO C
        where P.infection_case = C.infection_case and infection_group = 1
        group by infection_case, confirmed, C.province
        order by confirmed desc";
        mysqli_query($link, $sql);
    ?>
    <form method="GET" action="group_infection_q3.php">
    <input list="provinces" name="province">
    <datalist id="provinces">
        <option value="all"> All </option>
        <?php
            $sql = "select distinct Province from GROUP_INFECTION";
            $res = mysqli_query($link, $sql);
            
            while ($row = mysqli_fetch_assoc($res)) {
                
                foreach ($row as $key => $val) {
                    print "<option value=" . $val . ">" . $val . "</option>";
                }
            }
        ?>
    </datalist>
        </input>
    <input list="months" name="month">
    <datalist id="months">
        <option value="all"> All </option>
    <?php
            $sql = "select distinct month(First_Confirmed_Date) from GROUP_INFECTION order by month(First_Confirmed_Date)";
            $res = mysqli_query($link, $sql);
            while ($row = mysqli_fetch_assoc($res)) {
                
                foreach ($row as $key => $val) {
                    print "<option value=" . $val . ">" . $val . "</option>";
                }
            }
        ?>
    </datalist>
        </input>
    <input type="submit">
    </form>

    <?php
    $province = $_GET["province"];
    $month = $_GET["month"];
    $sql = "select count(*) as num from GROUP_INFECTION"; //where province='" . $province . "' and month(wdate)=" . $month;
    if ($province != "all" or $month != "all") {
        $sql = $sql . " where ";
    }
    if ($province != "all") {
        $sql = $sql . "province='" . $province . "'";

    }
    if ($month != "all") {
        $sql = $sql . " and month(First_Confirmed_Date)=" . $month;
    }
    
    

    $result = mysqli_query($link, $sql);
    $data = mysqli_fetch_assoc($result);
    ?>
    <p>
        <?php
            print "<h3> Selected Province : " . $province . ", Month : " . $month . "</h3>";
        ?>
        <h3>Weather table (Currently <?php echo $data['num']; ?>) rows in database </h3>
    </p>

    <table cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>Infection_case </th>
                <th>Province</th>
                <th>First_Confirmed_Date</th>
                <th>Total_confirmed_count</th>
            </tr>
        </thead>
        <tbody>
            <?php
            $sql = "select * from GROUP_INFECTION";// where province='" . $province . "' and month(wdate)=" . $month . " order by wdate";
            if ($province != "all" or $month != "all") {
                $sql = $sql . " where ";
            }
            if ($province != "all") {
                $sql = $sql . "province='" . $province . "'";
        
            }
            if ($month != "all") {
                $sql = $sql . " and month(First_Confirmed_Date)=" . $month;
            }
            
            $result = mysqli_query($link, $sql);
            while ($row = mysqli_fetch_assoc($result)) {
                print "<tr>";
                foreach ($row as $key => $val) {
                    print "<td>" . $val . "</td>";
                }
                print "</tr>";
            }
            ?>

        </tbody>
    </table>


</body>