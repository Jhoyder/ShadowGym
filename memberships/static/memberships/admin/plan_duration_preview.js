(function () {
  function toInt(value) {
    var parsed = parseInt(value, 10);
    return Number.isNaN(parsed) ? 0 : parsed;
  }

  function calculateDays(value, unit) {
    if (unit === "days") {
      return value;
    }
    if (unit === "months") {
      return value * 30;
    }
    if (unit === "years") {
      return value * 365;
    }
    return value;
  }

  function updatePreview() {
    var valueInput = document.getElementById("id_duration_value");
    var unitInput = document.getElementById("id_duration_unit");
    var preview = document.querySelector(".field-duration_days_preview .readonly");

    if (!valueInput || !unitInput || !preview) {
      return;
    }

    var value = Math.max(toInt(valueInput.value), 0);
    var days = calculateDays(value, unitInput.value);
    preview.textContent = String(days);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var valueInput = document.getElementById("id_duration_value");
    var unitInput = document.getElementById("id_duration_unit");

    if (valueInput) {
      valueInput.addEventListener("input", updatePreview);
      valueInput.addEventListener("change", updatePreview);
    }

    if (unitInput) {
      unitInput.addEventListener("change", updatePreview);
    }

    updatePreview();
  });
})();
