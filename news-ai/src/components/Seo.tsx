import { useContext } from 'react';
import { GlobalContext } from '@/context/GlobalContext';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export function Seo() {
  const globalContext = useContext(GlobalContext);

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  return (
    <div className="flex flex-col gap-2 p-4 rounded-md border m-4">
      <div className="flex flex-col gap-2">
        <div className="flex justify-between items-center space-x-2 pb-4">
          <Label htmlFor="a">Optimizar SEO</Label>
          <Switch id="a" />
        </div>
        <Label>Legibilidad</Label>
        <div className="w-full">
          <Select>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Elige una" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="light">Alta</SelectItem>
              <SelectItem value="dark">Media</SelectItem>
              <SelectItem value="system">Baja</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>
  );
}
