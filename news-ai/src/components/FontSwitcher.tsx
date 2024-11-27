import { useState } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
} from '@/components/ui/select';
import '@fontsource/roboto';
import '@fontsource/open-sans';
import '@fontsource/lato';
import '@fontsource/merriweather';
import '@fontsource/source-sans-pro';
import '@fontsource/nunito';
import '@fontsource/pt-sans';
import '@fontsource/pt-serif';
import '@fontsource/inter';

export const FontSwitcher = () => {
  const [font, setFont] = useState('Roboto');

  const fonts = [
    'Roboto',
    'Open Sans',
    'Lato',
    'Merriweather',
    'Source Sans Pro',
    'Nunito',
    'PT Sans',
    'PT Serif',
    'Inter',
  ];

  const handleFontChange = (selectedFont) => {
    setFont(selectedFont);
  };

  return (
    <div>
      <Select onValueChange={handleFontChange}>
        <SelectTrigger className="w-64">{font}</SelectTrigger>
        <SelectContent>
          {fonts.map((fontOption) => (
            <SelectItem key={fontOption} value={fontOption}>
              {fontOption}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};
