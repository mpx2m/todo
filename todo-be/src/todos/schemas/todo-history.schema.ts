import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument, Types } from 'mongoose';

export type TodoHistoryDocument = HydratedDocument<TodoHistory>;

@Schema({ timestamps: true })
export class TodoHistory {
  @Prop({ type: Types.ObjectId, ref: 'Todo', required: true })
  todoId: Types.ObjectId;

  @Prop({ required: true })
  changedAt: Date;

  @Prop({ type: Object, required: true })
  changes: Record<string, any>;
}

export const TodoHistorySchema = SchemaFactory.createForClass(TodoHistory);

// index for quick lookup by todo and recent changes first
TodoHistorySchema.index({ todoId: 1, changedAt: -1 });
