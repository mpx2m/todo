import {
  Body,
  Controller,
  Delete,
  Get,
  NotFoundException,
  Param,
  Patch,
  Post,
  Query,
} from '@nestjs/common';
import {
  ApiCreatedResponse,
  ApiOkResponse,
  ApiOperation,
  ApiTags,
} from '@nestjs/swagger';
import { AddDependenciesDto } from './dto/add-dependencies.dto';
import { CreateTodoDto } from './dto/create-todo.dto';
import { DependencyMutationResultDto } from './dto/dependency-mutation-result.dto';
import { SearchTodoDto } from './dto/search-todo.dto';
import {
  TodoResponseDto,
  TodoSearchResponseDto,
} from './dto/todo-response.dto';
import { TodoSubgraphDto } from './dto/todo-subgraph.dto';
import { UpdateTodoDto } from './dto/update-todo.dto';
import { MongoIdPipe } from './mongo-id.pipe';
import { TodosService } from './todos.service';

@ApiTags('todo')
@Controller('todo')
export class TodosController {
  constructor(private readonly todoService: TodosService) {}

  @Post()
  @ApiOperation({ summary: 'Create a todo' })
  @ApiCreatedResponse({ type: TodoResponseDto })
  create(@Body() createTodoDto: CreateTodoDto) {
    return this.todoService.create(createTodoDto);
  }

  @Get('search')
  @ApiOperation({ summary: 'Search todos' })
  @ApiOkResponse({ type: TodoSearchResponseDto })
  search(@Query() query: SearchTodoDto) {
    return this.todoService.search(query);
  }

  @Post(':id/dependencies')
  @ApiOperation({ summary: 'Add prerequisite dependencies to a todo' })
  @ApiOkResponse({ type: DependencyMutationResultDto })
  addDependencies(
    @Param('id', MongoIdPipe) id: string,
    @Body() body: AddDependenciesDto,
  ) {
    return this.todoService.addDependencies(id, body.prerequisiteIds ?? []);
  }

  @Delete(':id/dependencies')
  @ApiOperation({ summary: 'Remove prerequisite dependencies from a todo' })
  @ApiOkResponse({ type: DependencyMutationResultDto })
  removeDependencies(
    @Param('id', MongoIdPipe) id: string,
    @Body() body: AddDependenciesDto,
  ) {
    return this.todoService.removeDependencies(id, body.prerequisiteIds ?? []);
  }

  @Get(':id/dependencies')
  @ApiOperation({ summary: 'List prerequisite dependencies of a todo' })
  @ApiOkResponse({ type: TodoResponseDto, isArray: true })
  listDependencies(@Param('id', MongoIdPipe) id: string) {
    return this.todoService.listDependencies(id);
  }

  @Get(':id/dependents')
  @ApiOperation({ summary: 'List dependents of a todo' })
  @ApiOkResponse({ type: TodoResponseDto, isArray: true })
  listDependents(@Param('id', MongoIdPipe) id: string) {
    return this.todoService.listDependents(id);
  }

  @Get(':id/subgraph')
  @ApiOperation({ summary: 'Get the upstream and downstream graph of a todo' })
  @ApiOkResponse({ type: TodoSubgraphDto })
  async subgraph(@Param('id', MongoIdPipe) id: string) {
    const subgraph = await this.todoService.getSubgraph(id);
    if (!subgraph) {
      throw new NotFoundException(`Todo with id ${id} not found`);
    }
    return subgraph;
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get a todo by id' })
  @ApiOkResponse({ type: TodoResponseDto })
  async findOne(@Param('id', MongoIdPipe) id: string) {
    const todo = await this.todoService.findOne(id);
    if (!todo) {
      throw new NotFoundException(`Todo with id ${id} not found`);
    }
    return todo;
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update a todo' })
  @ApiOkResponse({ type: TodoResponseDto })
  async update(
    @Param('id', MongoIdPipe) id: string,
    @Body() updateTodoDto: UpdateTodoDto,
  ) {
    const todo = await this.todoService.update(id, updateTodoDto);
    if (!todo) {
      throw new NotFoundException(`Todo with id ${id} not found`);
    }
    return todo;
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Soft delete a todo' })
  @ApiOkResponse({ type: TodoResponseDto })
  async remove(@Param('id', MongoIdPipe) id: string) {
    const todo = await this.todoService.remove(id);
    if (!todo) {
      throw new NotFoundException(`Todo with id ${id} not found`);
    }
    return todo;
  }
}
