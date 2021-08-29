<?php
	use xPaw\MinecraftPing;
	use xPaw\MinecraftPingException;
	// Edit this ->
	define( 'MQ_SERVER_ADDR', '127.0.0.1' );
	define( 'MQ_SERVER_PORT', 25565 );
	define( 'MQ_TIMEOUT', 5 );
	// Edit this <-
	require __DIR__ . '/src/MinecraftPing.php';
	require __DIR__ . '/src/MinecraftPingException.php';
	$Timer = MicroTime( true );
	$Info = false;
	$Query = null;
	try{
		$Query = new MinecraftPing( MQ_SERVER_ADDR, MQ_SERVER_PORT, MQ_TIMEOUT );
		$Info = $Query->Query( );
		if( $Info === false ){
			/*
			 * If this server is older than 1.7, we can try querying it again using older protocol
			 * This function returns data in a different format, you will have to manually map
			 * things yourself if you want to match 1.7's output
			 *
			 * If you know for sure that this server is using an older version,
			 * you then can directly call QueryOldPre17 and avoid Query() and then reconnection part
			 */
			$Query->Close( );
			$Query->Connect( );
			$Info = $Query->QueryOldPre17( );
		}
	}
	catch( MinecraftPingException $e ){
		$Exception = $e;
	}
	if($Query !== null){
		$Query->Close( );
	}
	$Timer = Number_Format( MicroTime( true ) - $Timer, 4, '.', '' );
	if(isset($Exception)){
		$exception_msg= htmlspecialchars($Exception->getMessage());
		$json = json_encode(array('status' => 2));
		echo($json);
		exit();
	}
	if($Info!==false){
		foreach( $Info as $InfoKey => $InfoValue ){
			if( $InfoKey === 'description' ){
				$description = $InfoValue;
			}else if($InfoKey==='players'){
				$players=$InfoValue;
			}else if($InfoKey==='version'){
				$version=$InfoValue;
			}else if($InfoKey==='favicon'){
				$image=$InfoValue;
			}else{}
		}
		$json = json_encode(array('status' => 1, 'timer' => $Timer, 'description' => $description,'image' => $image, 'players' => $players, 'version' => $version));
		echo($json);
	}else{
		$json = json_encode(array('status' => 3));
		echo($json);
	}
?>