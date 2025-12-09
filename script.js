document.addEventListener("DOMContentLoaded", () => {
  const API = "http://127.0.0.1:5000";
  const plantContainer = document.getElementById("plantContainer");
  const favoritesContainer = document.getElementById("favoritesContainer");

  const searchInput = document.getElementById("searchInput");
  const searchBtn = document.getElementById("searchBtn");
  const filterLight = document.getElementById("filterLight");
  const filterBtn = document.getElementById("filterBtn");

  // Modal elements
  const modal = document.getElementById("detailsModal");
  const modalContent = document.getElementById("modalContent");
  const modalClose = document.getElementById("modalClose");

  // Load all plants and favorites initially
  fetchPlants();
  fetchFavorites();

  // Search button
  searchBtn.addEventListener("click", () => {
    const query = searchInput.value.trim();
    fetchPlants(query);
  });

  // Filter button (light only)
  filterBtn.addEventListener("click", () => {
    const light = filterLight.value || "";
    fetchFilteredPlants(light);
  });

  // Close modal
  modalClose.onclick = () => modal.style.display = "none";
  window.onclick = (e) => { if (e.target == modal) modal.style.display = "none"; }

  // Fetch all plants
  function fetchPlants(search = "") {
    const url = search ? `${API}/search?name=${encodeURIComponent(search)}` : `${API}/plants`;
    fetch(url)
      .then(res => res.json())
      .then(plants => renderPlants(plants))
      .catch(err => console.error(err));
  }

  // Fetch plants filtered by light
  function fetchFilteredPlants(light) {
    const params = new URLSearchParams();
    if (light) params.append("light", light);

    fetch(`${API}/filter?${params.toString()}`)
      .then(res => res.json())
      .then(plants => renderPlants(plants))
      .catch(err => console.error(err));
  }

  // Fetch favorites
  function fetchFavorites() {
    fetch(`${API}/favorites`) // You will need to create this endpoint
      .then(res => res.json())
      .then(plants => renderFavorites(plants))
      .catch(err => console.error(err));
  }

  // Render plants as cards
  function renderPlants(plants) {
    plantContainer.innerHTML = "";
    plants.forEach(plant => {
      const card = document.createElement("div");
      card.className = "plant-card";
      card.innerHTML = `
        <h3>${plant.name}</h3>
        <p><strong>Light:</strong> ${plant.light_type || "N/A"}</p>
        <div class="plant-buttons">
          <button onclick="showDetails(${plant.plant_id})">View Details</button>
          <button onclick="favoritePlant(${plant.plant_id})">⭐ Favorite</button>
        </div>
      `;
      plantContainer.appendChild(card);
    });
  }

  // Render favorites bar
  function renderFavorites(plants) {
    favoritesContainer.innerHTML = "";
    if (plants.length === 0) {
      favoritesContainer.textContent = "No favorite plants yet.";
      return;
    }
    plants.forEach(plant => {
      const card = document.createElement("div");
      card.className = "plant-card";
      card.innerHTML = `
        <h3>${plant.name}</h3>
        <div class="plant-buttons">
          <button onclick="showDetails(${plant.plant_id})">View Details</button>
          <button onclick="removeFavorite(${plant.plant_id})">❌ Remove</button>
        </div>
      `;
      favoritesContainer.appendChild(card);
    });
  }

  // Show plant details in modal
  window.showDetails = function(plant_id) {
    fetch(`${API}/plants/${plant_id}`)
      .then(res => res.json())
      .then(plant => {
        if (plant.error) {
          modalContent.innerHTML = `<p>${plant.error}</p>`;
        } else {
          modalContent.innerHTML = `
            <h2>${plant.name}</h2>
            <p><strong>Light:</strong> ${plant.light_type || "N/A"}</p>
            <p><strong>Watering:</strong> ${plant.watering_type || "N/A"}</p>
            <p><strong>Humidity:</strong> ${plant.humidity_type || "N/A"}</p>
            <p><strong>Temperature:</strong> ${plant.temperature_type || "N/A"}</p>
            <p><strong>Fertilizer:</strong> ${plant.fertilizer_type || "N/A"}</p>
            <p><strong>Pruning:</strong> ${plant.pruning_type || "N/A"}</p>
            <p><strong>Propagation:</strong> ${plant.propagation_type || "N/A"}</p>
          `;
        }
        modal.style.display = "block";
      });
  };

  // Add plant to favorites
  window.favoritePlant = function(plant_id) {
    fetch(`${API}/favorite/${plant_id}`, { method: "POST" })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        fetchFavorites(); // Refresh favorites bar
      })
      .catch(err => console.error(err));
  };

  // Remove plant from favorites
  window.removeFavorite = function(plant_id) {
    fetch(`${API}/favorite/${plant_id}`, { method: "DELETE" }) // You need to support DELETE in Flask
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        fetchFavorites(); // Refresh favorites bar
      })
      .catch(err => console.error(err));
  };
});
