const jsLang = document.getElementById("js-lang");
const handleChange = () => {
  const selected = jsLang.value;

  fetch(`/users/switch-language?lang=${selected}`).then(() =>
    window.location.reload()
  );
};
jsLang.addEventListener("change", handleChange);
