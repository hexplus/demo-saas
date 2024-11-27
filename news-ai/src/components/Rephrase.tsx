import { useContext, useEffect, useState } from 'react';
import { GlobalContext } from '@/context/GlobalContext';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Switcher } from './Switcher';

export function Rephrase() {
  const globalContext = useContext(GlobalContext);
  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }
  const {
    fetchStyles,
    fetchTones,
    fetchComplexities,
    styles,
    tones,
    complexities,
    setRephrase,
    content,
    isProcessing,
  } = globalContext;

  const [isChecked, setIsChecked] = useState(() => {
    return localStorage.getItem('rephrase') === 'true';
  });

  useEffect(() => {
    fetchStyles();
    fetchTones();
    fetchComplexities();
  }, []);

  useEffect(() => {
    localStorage.setItem('rephrase', isChecked);
    setRephrase(isChecked);
  }, [isChecked, setRephrase]);

  const handleRephrase = (e) => {
    setIsChecked(e);
  };

  return (
    <div className="flex flex-col gap-2 p-4 rounded-md border m-4">
      <div className="flex flex-col gap-2">
        <div className="flex justify-between items-center space-x-2 pb-4">
          <Label htmlFor="a">Cambiar redacción</Label>
          <Switch
            id="rephrase"
            onCheckedChange={handleRephrase}
            checked={isChecked}
            disabled={content.length === 0 || isProcessing}
          />
        </div>
        <Switcher
          isCollapsed={false}
          disabled={!isChecked || isProcessing}
          options={styles?.styles}
          contextProperty="Style"
          label="Estilo"
        />
        <Switcher
          isCollapsed={false}
          disabled={!isChecked || isProcessing}
          options={tones?.tones}
          contextProperty="Tone"
          label="Tono"
        />

        <Switcher
          isCollapsed={false}
          disabled={!isChecked || isProcessing}
          options={complexities?.complexities}
          contextProperty="Complexity"
          label="Complejidad"
        />
      </div>
    </div>
  );
}
