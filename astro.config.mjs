import { defineConfig } from "astro/config";
import alpinejs from "@astrojs/alpinejs"; // Импортируем интеграцию

export default defineConfig({
  // Добавляем Alpine в список интеграций
  integrations: [alpinejs()],
});
