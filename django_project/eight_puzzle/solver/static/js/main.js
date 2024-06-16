$(document).ready(function () {

  ///* ------------------- Random Solvable Example Generator -------------------*///
  $("#generate").click(function (e) {

    // If one of the random generator's radio buttons was checked
    if ($("input[name='randGenRadio']:checked").val() !== undefined) {

      // Gets the y, x position of an element in a state.
      function getPos(current_state, element) {
        for (let row = 0; row < current_state.length; row++) {
          if (current_state[row].includes(element)) {
            return [row, current_state[row].indexOf(element)];
          }
        }
      }

      // Generates random descendants for a state, where n is a random 
      // number that represents how far the descendants are.
      function genRandDescendants(current_state, n) {
        let childern = []; // only the children for each current state.
        let emptyPos = getPos(current_state, 0);
        let directions = { "UP": [-1, 0], "DOWN": [1, 0], "LEFT": [0, -1], "RIGHT": [0, 1] };
        for (let dir in directions) {
          let newPos = [emptyPos[0] + directions[dir][0], emptyPos[1] + directions[dir][1]];
          if ((0 <= newPos[0] && newPos[0] < current_state.length) && (0 <= newPos[1] && newPos[1] < current_state.length)) {
            let newState = JSON.parse(JSON.stringify(current_state));
            newState[emptyPos[0]][emptyPos[1]] = current_state[newPos[0]][newPos[1]];
            newState[newPos[0]][newPos[1]] = 0;
            childern.push(newState);
          }
        }
        n -= 1;
        if (n === 0) {
          // Return the children generated for the last chosen child.
          return childern;
        } else {
          // Pick a random child to generate its children next.
          return genRandDescendants(childern[Math.floor(Math.random() * (childern.length - 0) + 0)], n)
        }
      }

      // Generate Goal State values.
      let goalVals = [];
      if ($("#defaultGoal").is(':checked')) {
        goalVals = [1, 2, 3, 4, 5, 6, 7, 8, 0];
      } else if ($("#randomGoal").is(':checked')) {
        for (let i = 0; i < 9; i++) {
          let len = goalVals.length;
          while (len === goalVals.length) {
            let rand = Math.floor(Math.random() * 9);
            if (goalVals.includes(rand)) {
              continue;
            } else {
              goalVals.push(rand);
            }
          }
        }
      }
      // Fill the Goal State input boxes.
      let goalBoxes = $('textarea[name^="goal-"]');
      for (let i = 0; i < goalBoxes.length; i++) {
        goalBoxes[i].value = goalVals[i];
      }

      // Format like: [[],[],[]].
      goalVals = [goalVals.slice(0, 3), goalVals.slice(3, 6), goalVals.slice(6, 9)];
      // Generate random descendants that have an n distance from the goal.
      let n = Math.floor((Math.random() * 300));
      let randomDescendants = genRandDescendants(goalVals, n);
      // Pick one random descendant randomly from the returned list of random descendants.
      let initVals = randomDescendants[Math.floor(Math.random() * (randomDescendants.length - 0) + 0)];

      // Spread the nested lists to be easier to fill the Initial State input boxes.
      initVals = [...initVals[0], ...initVals[1], ...initVals[2]];
      let initBoxes = $('textarea[name^="initial-"]');
      for (let i = 0; i < initBoxes.length; i++) {
        initBoxes[i].value = initVals[i];
      }

      $("#reset").css('visibility', 'visible');
    }
  });

  ///*------------------- Puzzle Solve Button  -------------------*///
  $("#solve").click(function (e) {

    let init = [];
    let goal = [];

    /*------------- Validate Initial State Input -------------*/
    let check = [];
    let noInput = false;
    let notNumber = false;
    let duplicateVal = false;
    let zeroValMissing = false;
    let initBoxes = $('textarea[name^="initial-"]');
    for (let i = 0; i < initBoxes.length; i++) {
      init.push(initBoxes[i].value.trim());
    }
    for (let i = 0; i < init.length; i++) {
      if (init[i] === "") {
        noInput = true;
        break;
      } else {
        // Parse to int
        init[i] = parseInt(init[i]);
        if (isNaN(init[i])) {
          notNumber = true;
          break;
          // Check for duplicate values
        } else if (check.includes(init[i])) {
          duplicateVal = true;
          break;
        }
        check.push(init[i]);
      }
    }
    // Check that 0 was input
    if (!check.includes(0)) {
      zeroValMissing = true;
    }
    $("#reset").css('visibility', 'visible');
    $("#result").removeClass("showingSolution");
    // Show an error message if the input for Initial State was not valid
    if (noInput) {
      $("#result").empty().append("<span class='error'>Please input all values for Initial State.</span>");
    } else if (notNumber) {
      $("#result").empty().append("<span class='error'>Invalid input for Initial State:\n<br>(Only numbers are allowed).</span>");
    } else if (duplicateVal) {
      $("#result").empty().append("<span class='error'>Invalid input for Initial State:\n<br>(Duplicate values are not allowed).</span>");
    } else if (zeroValMissing) {
      $("#result").empty().append("<span class='error'>Invalid input for Initial State:\n<br>(The value 0 is required).</span>");
      // Initial state input was valid
    } else {
      $("#result").empty();

      /*------------- Validate Goal State Input -------------*/
      check = [];
      noInput = false;
      notNumber = false;
      duplicateVal = false;
      zeroValMissing = false;
      let notInInitial = false;
      let goalBoxes = $('textarea[name^="goal-"]');
      for (let i = 0; i < goalBoxes.length; i++) {
        goal.push(goalBoxes[i].value.trim());
      }
      for (let i = 0; i < goal.length; i++) {
        if (goal[i] === "") {
          noInput = true;
          break;
        } else {
          // Parse to int
          goal[i] = parseInt(goal[i]);
          if (isNaN(goal[i])) {
            notNumber = true;
            break;
            // Check that the goal state values are present in the initial state
          } else if (!init.includes(goal[i])) {
            notInInitial = true;
            break;
            // Check for duplicate values
          } else if (check.includes(goal[i])) {
            duplicateVal = true;
            break;
          }
          check.push(goal[i]);
        }
      }
      // Check that 0 was input
      if (!check.includes(0)) {
        zeroValMissing = true;
      }
      // Show an error message if the input for Goal State was not valid
      if (noInput) {
        $("#result").empty().append("<span class='error'>Please input all values for Goal State.</span>");
      } else if (notNumber) {
        $("#result").empty().append("<span class='error'>Invalid input for Goal State:\n<br>(Only numbers are allowed).</span>");
      } else if (notInInitial) {
        $("#result").empty().append("<span class='error'>Invalid input for Goal State:\n<br>(All values must be present in the initial state).</span>");
      } else if (duplicateVal) {
        $("#result").empty().append("<span class='error'>Invalid input for Goal State:\n<br>(Duplicate values are not allowed).</span>");
      } else if (zeroValMissing) {
        $("#result").empty().append("<span class='error'>Invalid input for Goal State:\n<br>(The value 0 is required).</span>");
        // Goal state input was valid
      } else {
        $("#result").empty();

        /*------------- Send Initial and Goal Data Using Ajax and Show Response Result -------------*/

        // Use a string formatted like: "1,2,3\n4,5,6\n7,8,0" for each 
        // of init and goal in order to send them in a GET request.
        let initStr = "";
        let goalStr = "";
        init = [init.slice(0, 3), init.slice(3, 6), init.slice(6, 9)];
        goal = [goal.slice(0, 3), goal.slice(3, 6), goal.slice(6, 9)];

        for (row = 0; row < init.length - 1; row++) {
          for (col = 0; col < init[0].length - 1; col++) {
            initStr += init[row][col] + ",";
            goalStr += goal[row][col] + ",";
          }
          initStr += init[row][col] + '\n';
          goalStr += goal[row][col] + '\n';
        }
        for (col = 0; col < init[0].length - 1; col++) {
          initStr += init[row][col] + ",";
          goalStr += goal[row][col] + ",";
        }
        initStr += init[row][col];
        goalStr += goal[row][col];

        $.ajax({
          type: "GET",
          url: "",
          data: { init: initStr, goal: goalStr },
          success: function (response) {
            $("#result").append(response.result).addClass("showingSolution");
          },
        });
      }
    }

  });

  ///*--------- Initial and Goal States Input Boxes ---------*///
  $("textarea").on({
    click: function () {
      this.focus();
      this.select();
    },
    keydown: function (e) {
      // If the tab key was pressed
      if (e.which === 9) {
        this.focus();
        this.select();
      }
    },
    focus: function () {
      this.select();
    },
    change: function () {
      if ($(this).val() !== "") {
        $("#reset").css('visibility', 'visible');
      } else {
        let noStateInput = true;
        let initBoxes = $('textarea[name^="initial-"]');
        let goalBoxes = $('textarea[name^="goal-"]');
        for (let i = 0; i < initBoxes.length; i++) {
          if (initBoxes[i].value !== "") {
            noStateInput = false;
            break;
          }
        }
        for (let i = 0; i < goalBoxes.length; i++) {
          if (goalBoxes[i].value !== "") {
            noStateInput = false;
            break;
          }
        }
        if (noStateInput && $("#result").is(":empty") && $("input[name='randGenRadio']:checked").val() === undefined)
          $("#reset").css('visibility', 'hidden');
      }
    }
  });

  ///*--------- Random Generator's Radio Buttons ---------*///
  $("input[name='randGenRadio']").change(function () {
    $("#reset").css('visibility', 'visible');
    $("#generate").removeClass("disabled");
  });

  ///*--------- Reset Button ---------*///
  $("#reset").click(function (e) {
    $("textarea").val("");
    $("#result").empty().removeClass("showingSolution");
    $('input[name="randGenRadio"]').prop('checked', false);
    $("#generate").addClass("disabled");
    $(this).css('visibility', 'hidden');
  });

  ///*--------- Ajax Events  ---------*///
  $(document).on({
    ajaxStart: function () {
      $("#solve").toggleClass("disabled");
      $("#solveBtn-text").html("Thinking...");
      $(".spinner-border").toggleClass("visually-hidden");
      $("#generate").addClass("disabled");
      $("textarea, input[name='randGenRadio']").prop('disabled', true);
      $("#reset").css('visibility', 'hidden');
    },
    ajaxStop: function () {
      $("#solve").toggleClass("disabled");
      $("#solveBtn-text").html("Solve");
      $(".spinner-border").toggleClass("visually-hidden");
      if ($("input[name='randGenRadio']:checked").val() !== undefined) {
        $("#generate").removeClass("disabled");
      }
      $("textarea, input[name='randGenRadio']").prop('disabled', false);
      $("#reset").css('visibility', 'visible');
    },
  });

  ///*--------- Back-to-Top Button ---------*///
  // When the user scrolls down 20px from the top of the document, show the button
  $(window).scroll(function () {
    if (document.body.scrollTop > 640 || document.documentElement.scrollTop > 640) {
      $("#btn-back-to-top").show();
    } else {
      $("#btn-back-to-top").hide();
    }
  });
  // When the user clicks on the button, scroll to the top of the document
  $("#btn-back-to-top").click(function () {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  });
});