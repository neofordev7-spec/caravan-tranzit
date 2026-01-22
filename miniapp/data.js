/**
 * CARAVAN TRANZIT - Data Configuration
 * Narxlar katalogi va boshqa statik ma'lumotlar
 */

// EPI-KOD xizmatlari narxlari
export const priceCatalog = {
  title: "EPI-KOD Xizmatlari",
  description: "Caravan Tranzit tomonidan tasdiqlangan narxlar",
  currency: "UZS",
  items: [
    { count: "1-2 partiya", price: 35000, label: "Jami" },
    { count: "3 partiya", price: 45000, label: "Jami" },
    { count: "4 partiya", price: 60000, note: "Donasi 15,000 so'mdan" },
    { count: "5 partiya", price: 75000, note: "Donasi 15,000 so'mdan" },
    { count: "6 partiya", price: 105000, note: "Donasi 17,500 so'mdan" },
    { count: "7 partiya", price: 126000, note: "Donasi 18,000 so'mdan" },
    { count: "8 partiya", price: 144000, note: "Donasi 18,000 so'mdan" },
    { count: "9 partiya", price: 180000, note: "Donasi 20,000 so'mdan" }
  ],
  contacts: {
    phone1: "+998 94 312 00 99",
    phone2: "+998 91 702 00 99"
  }
};

// Narxni formatlash funksiyasi
export function formatPrice(price) {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') + " so'm";
}

// Narxlar ro'yxatini HTML/text formatida olish
export function getPriceListText() {
  let text = `${priceCatalog.title}\n`;
  text += `${priceCatalog.description}\n\n`;

  priceCatalog.items.forEach(item => {
    text += `${item.count}: ${formatPrice(item.price)}`;
    if (item.note) {
      text += ` (${item.note})`;
    }
    text += '\n';
  });

  text += `\nBog'lanish:\n`;
  text += `${priceCatalog.contacts.phone1}\n`;
  text += `${priceCatalog.contacts.phone2}`;

  return text;
}

// Default export
export default priceCatalog;
