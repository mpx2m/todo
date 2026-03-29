import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { TodosService } from './todos.service';
import { TodosController } from './todos.controller';
import { Todo, TodoSchema } from './schemas/todo.schema';
import {
  TodoDependency,
  TodoDependencySchema,
} from './schemas/todo-dependency.schema';
import { TodoHistory, TodoHistorySchema } from './schemas/todo-history.schema';

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: Todo.name, schema: TodoSchema },
      { name: TodoDependency.name, schema: TodoDependencySchema },
      { name: TodoHistory.name, schema: TodoHistorySchema },
    ]),
  ],
  controllers: [TodosController],
  providers: [TodosService],
  exports: [TodosService],
})
export class TodosModule {}
