// Todo: Create a function that loads the country, state, city, zip

const countryStateInfo = {
    USA: {
      California: {
        "Los Angeles": ["90001", "90002", "90003", "90004"],
        "San Diego": ["92093", "92101"],
      },
      Texas: {
        Dallas: ["75201", "75202"],
        Austin: ["73301", "73344"],
      },
    },
    Germany: {
      Bavaria: {
        Munich: ["80331", "80333", "80335", "80336"],
        Nuremberg: ["90402", "90403", "90404", "90405"],
      },
      Hessen: {
        Frankfurt: ["60306", "60308", "60309", "60310"],
        Surat: ["55246", "55247", "55248", "55249"],
      },
    },
  };


  // Todo loader function

  window.onload = function(){
    const countrySelection = document.querySelector("#Country"),
    StateSelection = document.querySelector("#State"),
    citySelection = document.querySelector("#City"),
    zipSelection = document.querySelector("#Zip");
    console.log(countrySelection)




  };