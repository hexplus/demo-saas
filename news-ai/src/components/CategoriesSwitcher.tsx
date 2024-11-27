import { useState, useEffect, useContext } from 'react';
import { cn } from '@/lib/utils';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { GlobalContext } from '@/context/GlobalContext'; // Asegúrate de importar el contexto
import { LoadingSpinner } from './LoadingSpinner';

interface Category {
  label: string;
  slug: string;
}

interface CategoriesSwitcherProps {
  isCollapsed: boolean;
  categories: Category[];
}

export function CategoriesSwitcher({
  isCollapsed,
  categories,
}: CategoriesSwitcherProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>();

  const globalContext = useContext(GlobalContext);

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  const { fetchHeadlines, adapter, isLoadingCategories, isProcessing } =
    globalContext;

  const onChangeCategory = (e) => {
    setSelectedCategory(e);
    fetchHeadlines(adapter);
  };

  return (
    <>
      {isLoadingCategories && <LoadingSpinner />}
      {categories && (
        <Select
          defaultValue={selectedCategory}
          onValueChange={onChangeCategory}
          disabled={categories.length === 0 || isProcessing}
        >
          <SelectTrigger
            className={cn(
              'flex items-center gap-2 [&>span]:line-clamp-1 [&>span]:flex [&>span]:w-full [&>span]:items-center [&>span]:gap-1 [&>span]:truncate [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0',
              isCollapsed &&
                'flex h-9 w-9 shrink-0 items-center justify-center p-0 [&>span]:w-auto [&>svg]:hidden'
            )}
            aria-label="Seleccione fuente"
          >
            <SelectValue placeholder="Categoría">
              <span className={cn('ml-2', isCollapsed && 'hidden')}>
                {
                  categories.find(
                    (category) => category.label === selectedCategory
                  )?.label
                }
              </span>
            </SelectValue>
          </SelectTrigger>
          <SelectContent>
            {categories.map((category, index) => (
              <SelectItem key={index} value={category.label}>
                <div className="flex items-center gap-3 [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0 [&_svg]:text-foreground">
                  {category.label}
                </div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      )}
    </>
  );
}
