<head>
    <title> K_COVID19 TEAM6 </title>
</head>
<?php
    $link = mysqli_connect("127.0.0.1","userid","password", "k_covid19");
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
    <h3> Select number of Confirmed.</h3>
    <?php
        $sql="select count(*) as num from patientinfo";
        $result = mysqli_query($link, $sql);
        $data = mysqli_fetch_assoc($result);
    ?>
	
	<?php
		$selectOption = 0;
		if (!empty($_POST))
			$selectOption = $_POST['taskOption'];
		
		$opt = array('확진자 수', '100명 이상', '50~100명', '0~50명');
		print "
			<form action='' method='post'>
			<select name='taskOption'>";
		foreach($opt as $key => $val)
		{
			print "<option value=".$key;
			if ($selectOption==$key) echo ' selected';
			print ">".$val."</option>";
		}
		print "
			</select>
			<input type='submit' value='load'/>
			</form>";
	?>
	
    <p>
        <h3>Case Info table (Currently <?php echo $data['num']; ?>) cases in database </h3>
    </p>

    <table cellspacing="0" width="100%">
        <thead>
        <tr>
            <th>Case_Id</th>
            <th>province</th>
            <th>City</th>
			<th>Infection_Group</th>
            <th>Infection_Case</th>
			<th>Confirmed</th>
			<th>Latitude</th>
			<th>Longitude</th>
        </tr>
        </thead>
        <tbody>
            <?php
                $sql = "select * from caseinfo";
                $result = mysqli_query($link,$sql);
                while( $row = mysqli_fetch_assoc($result)  )
                {
					$stop = 0;
					if ($selectOption != 0)
					{
						switch(intval($selectOption))
						{
							case 1:
								if ($row['confirmed'] < 100)
								{
									$stop = 1;
								}
								break;
							case 2:
								if ($row['confirmed'] >= 100 or $row['confirmed'] < 50)
								{
									$stop = 1;
								}
								break;
							case 3:
								if ($row['confirmed'] >= 50)
								{
									$stop = 1;
								}
								break;
						}
						if ($stop == 1)
							continue;
					}
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
