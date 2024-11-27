import { useState, useContext, useEffect } from 'react';
import { cn } from '@/lib/utils';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { GlobalContext } from '@/context/GlobalContext'; // Asegúrate de importar el contexto

interface StylesSwitcherProps {
  isCollapsed: boolean;
  disabled: boolean;
  styles: {
    name: string;
    description: string;
  }[];
}

export function StyleSwitcher({ isCollapsed, disabled }: StylesSwitcherProps) {
  useEffect(() => {
    fetchStyles();
  }, []);

  const [selectedStyle, setSelectedStyle] = useState<string>('');
  // styles[0]?.name || ''

  const globalContext = useContext(GlobalContext);

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  const { fetchStyles, styles } = useContext(GlobalContext);

  return (
    styles && (
      <Select
        defaultValue={selectedStyle}
        onValueChange={setSelectedStyle}
        disabled={disabled}
      >
        <SelectTrigger
          className={cn(
            'flex items-center gap-2 [&>span]:line-clamp-1 [&>span]:flex [&>span]:w-full [&>span]:items-center [&>span]:gap-1 [&>span]:truncate [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0',
            isCollapsed &&
              'flex h-9 w-9 shrink-0 items-center justify-center p-0 [&>span]:w-auto [&>svg]:hidden'
          )}
          aria-label="Estilo de redacción"
        >
          <SelectValue placeholder="Estilo de redacción">
            {styles.find((style) => style.name === selectedStyle)?.name}
            <span className={cn('ml-2', isCollapsed && 'hidden')}>
              {styles.find((style) => style.name === selectedStyle)?.name}
            </span>
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          {styles.map((style) => (
            <SelectItem key={style.name} value={style.name}>
              <div className="flex items-center gap-3 [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0 [&_svg]:text-foreground">
                {style.name}
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    )
  );
}
