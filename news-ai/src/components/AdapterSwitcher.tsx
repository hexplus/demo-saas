import { useState, useContext } from 'react';
import { cn } from '@/lib/utils';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { GlobalContext } from '@/context/GlobalContext'; // Asegúrate de importar el contexto

interface AdapterSwitcherProps {
  isCollapsed: boolean;
  adapters: {
    name: string;
    code: string;
    country: string;
    language: string;
    icon: React.ReactNode;
  }[];
}

export function AdapterSwitcher({
  isCollapsed,
  adapters,
}: AdapterSwitcherProps) {
  const [selectedAdapter, setSelectedAdapter] = useState<string>(
    adapters[0]?.code || ''
  );

  const globalContext = useContext(GlobalContext);

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  const { fetchHeadlines, fetchCategories, isProcessing } = globalContext;

  const handleAdapterChange = (e) => {
    setSelectedAdapter(e);
    fetchHeadlines(e, '');
    fetchCategories(e);
  };

  return (
    adapters && (
      <Select
        defaultValue={selectedAdapter}
        onValueChange={handleAdapterChange}
        disabled={isProcessing}
      >
        <SelectTrigger
          className={cn(
            'flex items-center gap-2 [&>span]:line-clamp-1 [&>span]:flex [&>span]:w-full [&>span]:items-center [&>span]:gap-1 [&>span]:truncate [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0 max-w-xs',
            isCollapsed &&
              'flex h-9 w-9 shrink-0 items-center justify-center p-0 [&>span]:w-auto [&>svg]:hidden'
          )}
          aria-label="Fuente de Noticias"
          style={{ width: '158px', maxWidth: '158px' }}
        >
          <SelectValue placeholder="Fuente de Noticias">
            {adapters.find((adapter) => adapter.code === selectedAdapter)?.icon}
            <span className={cn('ml-2', isCollapsed && 'hidden')}>
              {
                adapters.find((adapter) => adapter.code === selectedAdapter)
                  ?.name
              }
            </span>
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          {adapters.map((adapter) => (
            <SelectItem key={adapter.code} value={adapter.code}>
              <div className="flex items-center gap-3 [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0 [&_svg]:text-foreground">
                {adapter.icon}
                {adapter.name}
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    )
  );
}
