			var video = document.getElementById('video');
			var canvas = document.getElementById('canvas');
			var context = canvas.getContext('2d');

			navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.oGetUserMedia || navigator.msGetUserMedia;

			if(navigator.getUserMedia){
				navigator.getUserMedia({video:true}, streamWebCam, throwError);
			}

			function streamWebCam (stream) {
				video.src = window.URL.createObjectURL(stream);
				video.play();
			}

			function throwError (e) {
				alert(e.name);
			}

			var video = document.getElementsByTagName("video")[0];
			video.setAttribute('height', '600');
			video.setAttribute('width', '900');
			// function snap () {
			// 	canvas.width = video.clientWidth;
			// 	canvas.height = video.clientHeight;
			// 	context.drawImage(video, 0, 0);
			// }
