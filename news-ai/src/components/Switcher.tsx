import { useState, useContext, useEffect } from 'react';
import { cn } from '@/lib/utils';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { GlobalContext } from '@/context/GlobalContext';
import { Label } from '@/components/ui/label';

interface Option {
  name: string;
  icon?: JSX.Element;
}

interface SwitcherProps<T extends Option> {
  isCollapsed: boolean;
  disabled: boolean;
  options: T[];
  contextProperty: keyof GlobalContextType;
  label?: string;
}

export function Switcher<T extends Option>({
  isCollapsed,
  disabled,
  options,
  contextProperty,
  label,
}: SwitcherProps<T>) {
  const globalContext = useContext(GlobalContext);

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  const { content } = globalContext;

  const setFunction = globalContext[`set${String(contextProperty)}`] as
    | ((value: string) => void)
    | undefined;

  const [selectedOption, setSelectedOption] = useState<string>('');

  useEffect(() => {
    const savedOption = localStorage.getItem(String(contextProperty)) || '';
    if (savedOption && savedOption !== selectedOption) {
      setSelectedOption(savedOption);
      setFunction?.(savedOption);
    }
  }, []);

  const handleChange = (value: string) => {
    setSelectedOption(value);
    localStorage.setItem(String(contextProperty), value);
    setFunction?.(value);
  };

  return (
    <>
      {label && <Label>{label}</Label>}
      <div className="w-full">
        <Select
          value={selectedOption}
          onValueChange={handleChange}
          disabled={disabled || content.length == 0}
        >
          <SelectTrigger
            className={cn(
              'flex items-center gap-2 [&>span]:line-clamp-1 [&>span]:flex [&>span]:w-full [&>span]:items-center [&>span]:gap-1 [&>span]:truncate [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0',
              isCollapsed &&
                'flex h-9 w-9 shrink-0 items-center justify-center p-0 [&>span]:w-auto [&>svg]:hidden'
            )}
            aria-label={label}
          >
            <SelectValue placeholder={`Elige ${label?.toLowerCase()}`}>
              {options &&
                options.find((option) => option.name === selectedOption)?.icon}
              <span className={cn('ml-2', isCollapsed && 'hidden')}>
                {options &&
                  options.find((option) => option.name === selectedOption)
                    ?.name}
              </span>
            </SelectValue>
          </SelectTrigger>
          <SelectContent>
            {options &&
              options.map((option) => (
                <SelectItem key={option.name} value={option.name}>
                  <div className="flex items-center gap-3 [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0 [&_svg]:text-foreground">
                    {option.icon}
                    {option.name}
                  </div>
                </SelectItem>
              ))}
          </SelectContent>
        </Select>
      </div>
    </>
  );
}
