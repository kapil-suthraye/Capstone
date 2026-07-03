import { Injectable, signal, computed } from '@angular/core';
import { EvaluationResult } from '../models/evaluation-result';

@Injectable({ providedIn: 'root' })
export class SessionService {
  // Private writable signals — only mutated through explicit methods
  private readonly _documentId = signal('');
  private readonly _namespace = signal('');
  private readonly _filename = signal('');
  private readonly _pdfPath = signal('');
  private readonly _diagnosis = signal<string | null>(null);
  /** All evaluations keyed by namespace so counts are always namespace-specific */
  private readonly _evaluationsByNs = signal<Record<string, EvaluationResult[]>>({});

  // Public readonly computed accessors
  readonly documentId = computed(() => this._documentId());
  readonly namespace = computed(() => this._namespace());
  readonly filename = computed(() => this._filename());
  readonly pdfPath = computed(() => this._pdfPath());
  readonly diagnosis = computed(() => this._diagnosis());

  /** Evaluations for the currently active namespace only */
  readonly evaluations = computed<EvaluationResult[]>(() => {
    const ns = this._namespace();
    return this._evaluationsByNs()[ns] ?? [];
  });

  setUpload(
    documentId: string,
    namespace: string,
    filename: string,
    pdfPath: string,
    diagnosis?: string | null,
  ): void {
    this._documentId.set(documentId);
    this._namespace.set(namespace);
    this._filename.set(filename);
    this._pdfPath.set(pdfPath);
    this._diagnosis.set(diagnosis ?? null);
  }

  /**
   * Restore a session from a previously reviewed claim (e.g. when the user
   * clicks "View" in the dashboard or observability table).
   * document_id is derived from the namespace prefix for legacy compatibility.
   */
  restoreClaim(
    namespace: string,
    filename: string,
    pdfPath: string,
    diagnosis?: string | null,
  ): void {
    this._documentId.set(namespace);   // namespace doubles as document_id
    this._namespace.set(namespace);
    this._filename.set(filename);
    this._pdfPath.set(pdfPath);
    this._diagnosis.set(diagnosis ?? null);
  }

  addEvaluation(result: EvaluationResult): void {
    const ns = this._namespace();
    if (!ns) return;
    this._evaluationsByNs.update(prev => {
      const existing = prev[ns] ?? [];
      const filtered = existing.filter(e => e.prompt_id !== result.prompt_id);
      return { ...prev, [ns]: [...filtered, result] };
    });
  }

  clear(): void {
    this._documentId.set('');
    this._namespace.set('');
    this._filename.set('');
    this._pdfPath.set('');
    this._diagnosis.set(null);
    // Keep evaluations history — user may navigate back to a previous claim
  }

  clearAll(): void {
    this._documentId.set('');
    this._namespace.set('');
    this._filename.set('');
    this._pdfPath.set('');
    this._diagnosis.set(null);
    this._evaluationsByNs.set({});
  }
}
