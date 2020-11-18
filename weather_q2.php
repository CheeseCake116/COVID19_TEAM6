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
    <form method="GET" action="weather_q2.php">
    <input list="provinces" name="province">
    <datalist id="provinces">
        <?php
            $sql = "select distinct province from weather";
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
    <?php
            $sql = "select distinct month(wdate) from weather order by month(wdate)";
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
    $sql = "select count(*) as num from weather where province='" . $province . "' and month(wdate)=" . $month;
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
                <th>Region Code </th>
                <th>Province</th>
                <th>Date</th>
                <th>Average Temp.</th>
                <th>Min Temp.</th>
                <th>Max Temp.</th>
            </tr>
        </thead>
        <tbody>
            <?php
            $sql = "select * from weather where province='" . $province . "' and month(wdate)=" . $month;
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