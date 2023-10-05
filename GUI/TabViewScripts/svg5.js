function svg5_Change_Tab(tab_id_to_open){
	document.getElementById("_Explore_Tab").style.display = 'none';


	document.getElementById("_Test_Tab").style.display = 'none';


	document.getElementById(tab_id_to_open).style.display = 'block';
}

function _Explore_Tab_Btn_Clicked(){ svg5_Change_Tab("_Explore_Tab"); On_Explore_Tab_Open();}


function _Test_Tab_Btn_Clicked(){ svg5_Change_Tab("_Test_Tab"); On_Test_Tab_Open();}



_Explore_Tab_Btn_Clicked();

_Test_Tab_Btn_Clicked();

