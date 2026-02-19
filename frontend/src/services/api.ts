export interface AnalysisResult {
    fairness_score: number;
    final_summary: string;
    key_takeaways: string[];
    recommendation: string;
    pros: string[];
    cons: string[];
    hidden_risks: string[];
    audio_url: string;
    clauses: Array<{
        category: string;
        risk_level: 'low' | 'medium' | 'high';
        text: string;
        summary: string;
    }>;
}

export const uploadFile = async (file: File, languageCode: string = "en-IN", speaker: string = "anushka"): Promise<AnalysisResult> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language_code', languageCode);
    formData.append('speaker', speaker);

    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Upload failed');
    }

    return response.json();
};
