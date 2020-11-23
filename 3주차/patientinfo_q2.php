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
    <h3> Select Sex and Age.</h3>
    <form method="GET" action="patientinfo_q2.php">
    <input list="sex_list" name="sex">
    <datalist id="sex_list">
        <option value="male"> male </option>
        <option value="female"> female </option>
    </datalist>
        </input>
    <input list="ages" name="age">
    <datalist id="ages">
    <?php
            $sql = "select distinct age from patientInfo where age is not null order by age";
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
    $sex = $_GET["sex"];
    $age = $_GET["age"];
    $sql = "select count(*) as num from patientInfo where sex='" . $sex . "' and age='" . $age ."'";
    $result = mysqli_query($link, $sql);
    $data = mysqli_fetch_assoc($result);
    ?>
    <p>
        <?php
            print "<h3> Selected Sex : " . $sex . ", Age : " . $age . "</h3>";
        ?>
        <h3>Weather table (Currently <?php echo $data['num']; ?>) rows in database </h3>
    </p>

    <table cellspacing="0" width="100%">
        <thead>
            <tr>
            <th>Patient_ID</th>
            <th>Sex</th>
            <th>Age</th>
            <th>Country</th>
            <th>province</th>
            <th>City</th>
            <th>Infection_Case</th>
            <th>Infected_by</th>
            <th>contact_number</th>
            <th>symptom_onset_date</th>
            <th>confirmed_date</th>
            <th>released_date</th>
            <th>deceased_date</th>
            <th>state</th>
            </tr>
        </thead>
        <tbody>
            <?php
            $sql = "select * from patientInfo where sex='" . $sex . "' and age='" . $age ."'";
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
