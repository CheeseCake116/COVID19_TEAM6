<head>
    <title> K_COVID19 TEAM6 </title>
</head>
<?php
$link = mysqli_connect("127.0.0.1", "userid", "password", "k_covid19");
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
    <form method="GET" action="">
		<b>병원 번호 : </b><input type='number' name="hospital_id" default='<?php print "0"?>'></input>
		<input type="submit"></input>
    </form>

    <?php
	$hospital_id = 0;
	if (!empty($_GET)){
		$hospital_id = $_GET["hospital_id"];
		$sql = "select count(*) as num from patientInfo where hospital_id='" . $hospital_id . "'";
	}
	else
		$sql = "select count(*) as num from patientInfo";
    $result = mysqli_query($link, $sql);
    $data = mysqli_fetch_assoc($result);
	
    ?>
    <p>
        <?php
			if (!empty($_GET))
				print "<h3> Selected Hospital_id : " . $hospital_id . "</h3>";
        ?>
        <h3>Patient table (Currently <?php echo $data['num']; ?>) rows in database </h3>
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
            <th>Hospital_id</th>
            </tr>
        </thead>
        <tbody>
            <?php
			if (!empty($_GET))
				$sql = "select * from patientInfo where hospital_id='" . $hospital_id . "'";
			else
				$sql = "select * from patientInfo";
            $result = mysqli_query($link, $sql);
            while ($row = mysqli_fetch_assoc($result)) {
                print "<tr>";
                foreach ($row as $key => $val) {
					//if ($key == 'Hospital_id')
					//	print "<td><a link='https://map.kakao.com/link/map/" . . "'>" . $val . "</a></td>";
                    //else
						print "<td>" . $val . "</td>";
                }
                print "</tr>";
            }
            ?>

        </tbody>
    </table>


</body>
