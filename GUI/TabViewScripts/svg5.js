function svg5_Change_Tab(tab_id_to_open){
	document.getElementById("svg5_frame0").style.display = 'none';


	document.getElementById("svg5_frame1").style.display = 'none';


	document.getElementById(tab_id_to_open).style.display = 'block';
}

function svg5_frame0_Btn_Clicked(){ svg5_Change_Tab("svg5_frame0"); }


function svg5_frame1_Btn_Clicked(){ svg5_Change_Tab("svg5_frame1"); }



svg5_frame0_Btn_Clicked();

svg5_frame1_Btn_Clicked();

