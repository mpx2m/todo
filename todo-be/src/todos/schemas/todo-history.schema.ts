import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument, Types } from 'mongoose';
import { TodoHistoryChangeBy, TodoStatus } from '../types';

export type TodoHistoryDocument = HydratedDocument<TodoHistory>;

@Schema({ timestamps: true })
export class TodoHistory {
  @Prop({ type: Types.ObjectId, ref: 'Todo', required: true })
  todoId: Types.ObjectId;

  @Prop({
    type: String,
    enum: Object.values(TodoStatus),
    required: true,
  })
  from: TodoStatus;

  @Prop({
    type: String,
    enum: Object.values(TodoStatus),
    required: true,
  })
  to: TodoStatus;

  @Prop({
    type: String,
    enum: Object.values(TodoHistoryChangeBy),
    required: true,
  })
  by: TodoHistoryChangeBy;
}

export const TodoHistorySchema = SchemaFactory.createForClass(TodoHistory);

TodoHistorySchema.index({ todoId: 1, createdAt: -1 });
