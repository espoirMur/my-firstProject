 var frameApp = new frameApi.FrameApp({
          hash: $('#eahash').val()
      });

      frameApp.bind(FrameApp.EVENT_ERROR, function(e) {
          alert(e.message);
      });

      frameApp.bind(FrameApp.EVENT_LOADING_STARTED, function() {
        console.info('Loading started');
      });

      frameApp.bind(FrameApp.EVENT_LOADING_DONE, function() {
        console.info('Loading done.');
      });

      frameApp.bind(FrameApp.EVENT_CLOSED, function() {
        console.info('Session closed.');
      });

      frameApp.bind(FrameApp.EVENT_BROADCAST_SESSION_ID, function(sessionId) {
        console.info('Broadcast session id: ' + sessionId);
      });

      frameApp.bind(FrameApp.EVENT_BROADCAST_SHARE_URL, function(url) {
        console.info('Broadcast share url: ' + url);
      });

      frameApp.bind(FrameApp.EVENT_TERMINAL_SHOWN, function() {
        console.info('Terminal shown!');
      });

      frameApp.bind(FrameApp.EVENT_OPEN_URL, function(url) {
        console.info("Open url: " + url);
      });

      $(document).ready(function() {

        frameApp.bind(FrameApp.EVENT_READY, function() {

          $('#eahash').on('blur', function() {
            initializeFrameApp();
          });

          $("#start_app").click(function() {
            frameApp.startSession();
          });

          $('#start_app_no_player').click(function() {
            frameApp.startSession({
              connectOnStart: false,
            });
          });

          $('#connect').click(function() {
              frameApp.connect();
          });

          $('#resume').click(function() {
            frameApp.resumeSession(Cookies.get("sessionId"));
          });

          $('#resume_no_app_player').click(function() {
            var config = {
              connectOnStart: false
            };
            frameApp.resumeSession(Cookies.get('sessionId'), config);
          });

          $('#save_session_id').click(function() {
            Cookies.set('sessionId', frameApp.sessionId);
          });

          // Called each 3 seconds to return basic session parameters
          setInterval(function() {
            console.log("Getting session id: " + frameApp.sessionId);

            frameApp.getCapacityInfoAsync().then(function(capacityInfo) {
              console.log("Capacity info received:");
              console.log(capacityInfo);

              var props = ['available_instances', 'running_instances', 'coming_soon'];
              var stats = [];
              for(var i = 0; i < props.length; i++) {
                var property = props[i];
                stats.push(property + ': ' + capacityInfo[property]);
              }

              $('#capacity_info').html(stats.join('<br>'));
            });
          }, 3000);
        });
      });
