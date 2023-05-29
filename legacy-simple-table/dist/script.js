// init variables
let stats;
let batting = {};
let fielding = {};
let pitching = {};
let misc = {};

// Get references to the dropdown elements
const playerDropdown = document.getElementById("playerDropdown");
playerDropdown.value = "all";

const statTypeDropdown = document.getElementById("statTypeDropdown");
statTypeDropdown.value = "Batting";

// ref stat table
const statTable = document.getElementById("statTable");

// fetch from api
fetch(
  "https://api.projectrio.app/stats/?by_char=1&tag=legacymodestarsoff&by_user=1"
)
  .then((response) => response.json())
  .then((data) => {
    stats = data.Stats;

    // iterate over stats and group by category of stat
    for (let player in stats) {
      batting[player] = {};
      misc[player] = {};
      fielding[player] = {};
      pitching[player] = {};

      // iterate to include by character
      for (let character in stats[player]) {
        batting[player][character] = stats[player][character]["Batting"];
        misc[player][character] = stats[player][character]["Misc"];
        fielding[player][character] = stats[player][character]["Fielding"];
        pitching[player][character] = stats[player][character]["Pitching"];
      }

      // Populate the player dropdown menu with options
      const option = document.createElement("option");
      option.value = player;
      option.text = player;
      // append to dropdown
      playerDropdown.appendChild(option);
    }

    // Populate the stat type dropdown menu with options
    const statTypes = ["Batting", "Fielding", "Pitching", "Misc"];
    for (let statType of statTypes) {
      const option = document.createElement("option");
      option.value = statType;
      option.text = statType;
      // append to dropdown
      statTypeDropdown.appendChild(option);
    }

    // Add an "All" option to the player dropdown
    const allOption = document.createElement("option");
    allOption.value = "all";
    allOption.text = "All Players";
    // append to dropdown
    playerDropdown.appendChild(allOption);

    // Alphabetize options
    const playerOptions = Array.from(playerDropdown.options);
    playerOptions.sort((a, b) => a.textContent.localeCompare(b.textContent));

    playerDropdown.innerHTML = "";

    // Append the sorted option elements back to the select element
    playerOptions.forEach((option) => {
      playerDropdown.appendChild(option);
    });

    const statOptions = Array.from(statTypeDropdown.options);
    statOptions.sort((a, b) => a.textContent.localeCompare(b.textContent));

    // Remove existing options from the select element
    statTypeDropdown.innerHTML = "";

    // Append the sorted option elements back to the select element
    statOptions.forEach((option) => {
      statTypeDropdown.appendChild(option);
    });

    playerDropdown.options[0].selected = true;
    statTypeDropdown.options[0].selected = true;

    // Add event listener to the dropdowns
    playerDropdown.addEventListener("change", handleDropdownChange);
    statTypeDropdown.addEventListener("change", handleDropdownChange);

    // Event handler for dropdown change
    function handleDropdownChange() {
      // Get the selected player and stat type
      const selectedPlayer = playerDropdown.value;
      const selectedStatType = statTypeDropdown.value;

      // Check if the "All Players" option is selected - USELESS RIGHT NOW
      if (selectedPlayer === "all") {
        // playerLabel.innerHTML = 'All Players';
        statTable.innerHTML = "ALL PLAYERS TABLE IS WIP";
        // Handle the case when "All Players" is selected
      } else {
        // Get the corresponding stats based on the selected options
        let selectedStats;
        if (selectedStatType === "Batting") {
          selectedStats = batting[selectedPlayer];
        } else if (selectedStatType === "Fielding") {
          selectedStats = fielding[selectedPlayer];
        } else if (selectedStatType === "Pitching") {
          selectedStats = pitching[selectedPlayer];
        } else if (selectedStatType === "Misc") {
          selectedStats = misc[selectedPlayer];
        }

        // Clear table div
        statTable.innerHTML = "";

        // Create table element
        const table = document.createElement("table");
        table.classList.add("statTable");

        // Create thead and header row
        const thead = table.createTHead();
        const headerRow = thead.insertRow();

        // add character names (goes outside of specific stat types since it applies universally)
        headerRow.insertCell().textContent = "Character Name";

        // batting headers
        if (selectedStatType === "Batting") {
          headerRow.insertCell().textContent = "At Bats";
          headerRow.insertCell().textContent = "AVG";
          headerRow.insertCell().textContent = "OBP";
          headerRow.insertCell().textContent = "SLG";
          headerRow.insertCell().textContent = "OPS";
        }

        // fielding headers
        else if (selectedStatType === "Fielding") {
          headerRow.insertCell().textContent = "Bobbles";
          headerRow.insertCell().textContent = "Bobbles/Pitch";
          headerRow.insertCell().textContent = "Outs/Pitch";
          headerRow.insertCell().textContent = "Best Position by Outs/Pitch";
          headerRow.insertCell().textContent = "Wall Jumps";
        }

        // pitching headers
        else if (selectedStatType === "Pitching") {
          headerRow.insertCell().textContent = "Batters Faced";
          headerRow.insertCell().textContent = "Runs Allowed";
          headerRow.insertCell().textContent = "Opponent Avg";
          headerRow.insertCell().textContent = "7-inning ERA";
          headerRow.insertCell().textContent = "WHIP";
          headerRow.insertCell().textContent = "K%";
        }

        // misc headers
        else if (selectedStatType === "Misc") {
          headerRow.insertCell().textContent = "Home Win Rate";
          headerRow.insertCell().textContent = "Total Home Games";
          headerRow.insertCell().textContent = "Away Win Rate";
          headerRow.insertCell().textContent = "Total Away Games";
          headerRow.insertCell().textContent = "Total Games Played";
          headerRow.insertCell().textContent = "Total Win Rate";
        }

        // create tbody and rows (one per char)
        const tbody = table.createTBody();

        for (let character in selectedStats) {
          const characterStats = selectedStats[character];

          const row = tbody.insertRow();
          row.insertCell().textContent = character;

          // batting stats
          if (selectedStatType === "Batting") {
            const atBats = characterStats["summary_at_bats"];
            const hits = characterStats["summary_hits"];
            const doubles = characterStats["summary_doubles"];
            const triples = characterStats["summary_triples"];
            const homeRuns = characterStats["summary_homeruns"];
            const walks = characterStats["summary_walks_bb"];
            const hitByPitch = characterStats["summary_walks_hbp"];

            const singles = hits - doubles - triples - homeRuns;
            const totalBases =
              singles + 2 * doubles + 3 * triples + 4 * homeRuns;

            const battingAverage = hits / atBats;
            const onBasePercentage =
              (hits + walks + hitByPitch) / (atBats + walks + hitByPitch);
            const sluggingPercentage = totalBases / atBats;
            const onBasePlusSlugging = onBasePercentage + sluggingPercentage;

            row.insertCell().textContent = atBats;
            row.insertCell().textContent = battingAverage.toFixed(3);
            row.insertCell().textContent = onBasePercentage.toFixed(3);
            row.insertCell().textContent = sluggingPercentage.toFixed(3);
            row.insertCell().textContent = onBasePlusSlugging.toFixed(3);
          }
          // pitching stats
          if (selectedStatType === "Pitching") {
            const battersFaced = characterStats["batters_faced"];
            const runsAllowed = characterStats["runs_allowed"];
            const outsPitched = characterStats["outs_pitched"];
            const walksBB = characterStats["walks_bb"];
            const walksHBP = characterStats["walks_hbp"];
            const hitsAllowed = characterStats["hits_allowed"];
            const strikeoutsPitched = characterStats["strikeouts_pitched"];
            const oppAvg =
              hitsAllowed / (battersFaced - walksBB - walksHBP) || 0;
            const era = (runsAllowed / (outsPitched / 3)) * 7 || 0;
            const whip =
              (walksBB + walksHBP + hitsAllowed) / (outsPitched / 3) || 0;
            const kPercent = strikeoutsPitched / battersFaced || 0;

            row.insertCell().textContent = battersFaced;
            row.insertCell().textContent = runsAllowed;
            row.insertCell().textContent = oppAvg.toFixed(3);
            row.insertCell().textContent = era.toFixed(2);
            row.insertCell().textContent = whip.toFixed(2);
            row.insertCell().textContent = `${(kPercent * 100).toFixed(2)}%`;
          }

          // fielding stats
          if (selectedStatType === "Fielding") {
            const bobbles = characterStats["bobbles"] || 0;
            const wallJumps = characterStats["wall_jumps"] || 0;
            let totalPitches = 0;
            let totalOuts = 0;
            let bestPos = "";
            let bestPosRatio = 0;
            for (const key in characterStats) {
              // add total pitches
              if (key.startsWith("pitches_per_")) {
                totalPitches += characterStats[key];
              }

              // get outs / pitches by iterating over both
              if (key.startsWith("outs_per_")) {
                totalOuts += characterStats[key];

                const pitchKey = key.replace("outs_per_", "pitches_per_");
                const outs = characterStats[key];
                const pitches = characterStats[pitchKey];

                if (pitches !== 0) {
                  const ratio = outs / pitches;
                  if (ratio > bestPosRatio) {
                    bestPosRatio = ratio;
                    bestPos = key.replace("outs_per_", "");
                  }
                }
              }
            }
            let bobblesPerPitch = 0;
            let outsPerPitch = 0;
            if (totalPitches > 0) {
              bobblesPerPitch = bobbles / totalPitches;
              outsPerPitch = totalOuts / totalPitches;
            }

            row.insertCell().textContent = bobbles;
            row.insertCell().textContent = bobblesPerPitch.toFixed(3);
            row.insertCell().textContent = outsPerPitch.toFixed(3);
            row.insertCell().textContent = bestPos.toUpperCase();
            row.insertCell().textContent = wallJumps;
          }

          // misc stats
          if (selectedStatType === "Misc") {
            const homeWins = characterStats["home_wins"];
            const homeLosses = characterStats["home_loses"];
            const totalHomeGames = homeWins + homeLosses;
            const homeWinRate = homeWins / totalHomeGames || 0;
            const awayWins = characterStats["away_wins"];
            const awayLosses = characterStats["away_loses"];
            const totalAwayGames = awayWins + awayLosses;
            const awayWinRate = awayWins / totalAwayGames || 0;
            const totalGames = totalHomeGames + totalAwayGames;
            const totalWinRate = (awayWins + homeWins) / totalGames || 0;

            row.insertCell().textContent = `${(homeWinRate * 100).toFixed(2)}%`;
            row.insertCell().textContent = totalHomeGames;
            row.insertCell().textContent = `${(awayWinRate * 100).toFixed(2)}%`;
            row.insertCell().textContent = totalAwayGames;
            row.insertCell().textContent = totalGames;
            row.insertCell().textContent = `${(totalWinRate * 100).toFixed(
              2
            )}%`;
          }
        }

        // append table to page
        statTable.appendChild(table);

        // add tablesorter
        $(table).tablesorter({
          widgets: ["zebra"]
        });
      }
    }
  })
  .catch((error) => console.error("Error:", error));