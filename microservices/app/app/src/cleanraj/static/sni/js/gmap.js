/*		
function take_snapshot() {
	Webcam.snap( function(data_uri) {
		document.getElementById('my_result').innerHTML = '<img src="'+data_uri+'"/>';
	} );
}
*/
// global variable to close the
var span;


function initMap() 
{		
        var uluru = {lat: 24.571270, lng: 73.691544};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 20,
          center: uluru,
          disableDefaultUI: true
        });

        user_location_window = new google.maps.InfoWindow;

		if (navigator.geolocation) {
	          navigator.geolocation.getCurrentPosition(function(position) {
	            var pos = {
	              lat: position.coords.latitude,
	              lng: position.coords.longitude
	            };
	            user_location_window.setPosition(pos);
	            user_location_window.setContent('your location');
	            user_location_window.open(map);
	            map.setCenter(pos);
	          }, function() {
	            handleLocationError(true);
	          });

	    } 
	    else 
	    {
	          // Browser doesn't support Geolocation
	          handleLocationError(false);
	    }
      

        function handleLocationError(browserHasGeolocation) {
	        if(browserHasGeolocation)
	        {
	        	console.log("user hasn't given location permission.");
	        }
	        else
	        {
	        	alert("your browser is outdated.");
	        }
        }


        // load all points
        $.ajax({
			    url: "/showcords/",
			    type:"GET",
			  }).done(function(data){
		     //alert(data);

		    var cords_data = JSON.parse(data);

		    var markers = new Array(1000);
		    var latarray = new Array(1000);
		    var lonarray = new Array(1000);
		    var pkarray = new Array(1000);


			var modal = document.getElementById('myModal');
			var mapmodal = document.getElementById('map');
			var modalImg = document.getElementById("img01");


			// store lan lon in arrays
		    for(var i=0; i<cords_data.length; i++)
		    {
		    	latarray[i] = cords_data[i].fields.lat;
		    	lonarray[i] = cords_data[i].fields.lon;
		    	pkarray[i] = cords_data[i].pk;
		    }

		    for(var i=0; i<cords_data.length; i++)
		    {

		    	
			    markers[i] = new google.maps.Marker({
		          position: {lat: latarray[i], lng: lonarray[i]},
		          map: map,
		          icon:'/site_media/media/trash-can.png'
		        });

		        markers[i].addListener('click', function(e){
					
					modal.style.display = "block";

					parentDOM = document.getElementById('myModal');
					span = parentDOM.getElementsByClassName('close')[0];

					var captioncontent = document.getElementById("caption");

					
					

					// When the user clicks on <span> (x), close the modal
					span.onclick = function() {
						var modal = document.getElementById('myModal');
						modal.style.display = "none";
					}
					  

					//console.log(markers[0].position.lat);

					var latlon = e.latLng;
					console.log(latlon.lat(), latlon.lng());

					var location_can_be_remove, index_marker_to_be_deleted;
					for(var j=0; j<cords_data.length; j++)
					{
						if(latarray[j] == latlon.lat() && lonarray[j] == latlon.lng())
						{
							modalImg.src = cords_data[j].fields.garbage_pic;
							location_can_be_remove=pkarray[j];
							index_marker_to_be_deleted = j;
							if(captioncontent)
							{
								captioncontent.innerHTML = "<button type='button'>REMOVE</button>";									
							}
						}
					}
					if(location_can_be_remove && captioncontent)
					{
						captioncontent.addEventListener('click', function(){
									$.ajax({
									    url: "/removelocation/",
									    type:"POST",
									    data: {pk:location_can_be_remove}
									  }).done(function(data){
									     modal.style.display = "none";
									     console.log('deleted');
									     markers[index_marker_to_be_deleted].setMap(null);
								    });


								}, false);
					}
    				

				});
		    }


		  });

        map.addListener('dblclick', function(e) {

        	// open infowindow
		    var new_marker = placeMarkerAndPanTo(e.latLng, map);

		});

		function placeMarkerAndPanTo(latLng, map) {


		  var marker = new google.maps.Marker({
		    position: latLng,
		    map: map,
		    icon:'/site_media/media/trash-can.png'
		  });
		  

          infowindow_new.open(map, marker);

          
		  console.log(latLng.lat(), latLng.lng());

		  const fileInput = document.getElementById('file-input');

		  

		  fileInput.addEventListener('change', (e) => {
		  	file = e.target.files[0];
		  	console.log(file.name);
		  	
		  	

		  	var reader = new window.FileReader();	
		  	reader.readAsDataURL(file); 
		  	
		  	
			reader.onloadend = function() {
                base64data = reader.result;                
                //console.log(base64data);

                $.ajax({
				    url: "/savecords/",
				    type:"POST",
				    data: {lan:latLng.lat(),lon:latLng.lng(), image:base64data}
				  }).done(function(data){
			     //alert(data);
				     marker.addListener('click', function(){

				     	var modal = document.getElementById('myModal');
				     	modal.style.display = "block";

						parentDOM = document.getElementById('myModal');
						span = parentDOM.getElementsByClassName('close')[0];

						var modalImg = document.getElementById("img01");
						modalImg.src=base64data;

						var captioncontent = document.getElementById("caption");

						
						

						// When the user clicks on <span> (x), close the modal
						span.onclick = function() {
							var modal = document.getElementById('myModal');
							modal.style.display = "none";
						}
			     });
			     console.log(data);
			    });
  			}

 			infowindow_new.close();
			  
		  });
		  return marker;
		}
		

		var infowindow_new = new google.maps.InfoWindow({
		  content:"<input type='file' accept='image/*' id='file-input' capture>"
		});



}


