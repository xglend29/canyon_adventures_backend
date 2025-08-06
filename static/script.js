function calculatePrice() {
  const adultsInput = document.getElementById("adults");
  const childrenInput = document.getElementById("children");
  const tourSelect = document.getElementById("tour");

  if (!adultsInput || !childrenInput || !tourSelect) return;

  const adults = parseInt(adultsInput.value) || 0;
  const children = parseInt(childrenInput.value) || 0;
  const tour = tourSelect.value;

  let pricePerAdult = 0;
  let pricePerChild = 0;

  if (tour === "osumi") {
    pricePerAdult = 70;
    pricePerChild = 40;
  }

  const total = (adults * pricePerAdult) + (children * pricePerChild);
  document.getElementById("price").textContent = `€${total}`;
}

// Lidh evente
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("reservation-form");
  if (form) {
    ["input", "change"].forEach(evt => {
      form.addEventListener(evt, calculatePrice);
    });
  }
});
