import { useContext, useEffect, useState } from 'react';
import { GlobalContext } from '@/context/GlobalContext';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Switcher } from './Switcher';

export function Summary() {
  const globalContext = useContext(GlobalContext);
  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }
  const {
    setSummary,
    fetchSummaryLengths,
    fetchSummaryTypes,
    summaryLengths,
    summaryTypes,
    content,
    isProcessing,
  } = globalContext;

  const [isChecked, setIsChecked] = useState(() => {
    return localStorage.getItem('summary') === 'true';
  });

  useEffect(() => {
    fetchSummaryTypes();
    fetchSummaryLengths();
  }, []);

  useEffect(() => {
    localStorage.setItem('summary', isChecked);
    setSummary(isChecked);
  }, [isChecked, setSummary]);

  const handleRephrase = (checked) => {
    setIsChecked(checked);
  };

  return (
    <div className="flex flex-col gap-2 p-4 rounded-md border m-4">
      <div className="flex flex-col gap-2">
        <div className="flex justify-between items-center space-x-2 pb-4">
          <Label htmlFor="a">Resumir</Label>
          <Switch
            id="summary"
            checked={isChecked}
            onCheckedChange={handleRephrase}
            disabled={content.length === 0 || isProcessing}
          />
        </div>
        <Switcher
          isCollapsed={false}
          options={summaryTypes?.summary_types}
          contextProperty="SummaryType"
          label="Tipo"
          disabled={!isChecked || isProcessing}
        />
        <Switcher
          isCollapsed={false}
          options={summaryLengths?.summary_lengths}
          contextProperty="SummaryLength"
          label="Longitud"
          disabled={!isChecked || isProcessing}
        />
        {/* <Switcher
          isCollapsed={false}
          disabled={false}
          options={tones?.tones}
          contextProperty="Tone"
          label="Tono"
        />

        <Switcher
          isCollapsed={false}
          disabled={false}
          options={complexities?.complexities}
          contextProperty="Complexity"
          label="Complejidad"
        /> */}
      </div>
    </div>
  );
}
